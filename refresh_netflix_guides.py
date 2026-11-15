#!/usr/bin/env python3
"""Refresh a small public guide index, preserving last-known-good data on failure."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'netflix-guides.json'
MONTHS = 'January February March April May June July August September October November December'.split()
KINDS = {'coming': 'coming-soon', 'leaving': 'leaving-soon'}
HEADERS = {'User-Agent': 'Mozilla/5.0',
           'Accept': 'application/rss+xml,application/xml;q=0.9,*/*;q=0.8'}


def parse_feed(raw, kind):
    items = ET.fromstring(raw).findall('.//item')
    stem = 'whats-coming-to-netflix' if kind == 'coming' else 'whats-leaving-netflix'
    pattern = re.compile(r'https://www[.]whats-on-netflix[.]com/' + KINDS[kind] + '/'
                         + stem + r'(?:-in)?-([a-z]+)-(20[0-9]{2})/')
    guides = {}
    for item in items:
        url = item.findtext('link') or ''
        match = pattern.fullmatch(url)
        if match and match[1].capitalize() in MONTHS:
            guides[f'{kind}:{match[1].capitalize()}-{match[2]}'] = url
    if not guides:
        raise ValueError(f'No monthly US guides in {kind} feed')
    return guides


def fetch(kind):
    url = 'https://www.whats-on-netflix.com/' + KINDS[kind] + '/feed/'
    error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=15) as response:
                return kind, parse_feed(response.read(), kind), None
        except Exception as exc:
            error = type(exc).__name__ + ': ' + str(exc)
            if attempt < 2:
                time.sleep(1)
    return kind, None, error


def merge(existing, results, now):
    data = json.loads(json.dumps(existing))
    data.update(schema=1, region='US', last_attempt_at=now)
    data.setdefault('guides', {})
    data.setdefault('fetched_at', {})
    data['errors'] = {}
    successes = 0
    for kind, guides, error in results:
        if guides:
            data['guides'].update(guides)
            data['fetched_at'][kind] = now
            successes += 1
        else:
            data['errors'][kind] = error
    if successes:
        data['updated_at'] = now
    if not data['guides']:
        raise ValueError('No usable guides; refusing to publish an empty index')
    return data


def main():
    existing = json.loads(DATA.read_text()) if DATA.exists() else {}
    results = list(ThreadPoolExecutor(max_workers=2).map(fetch, KINDS))
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    data = merge(existing, results, now)
    temporary = DATA.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    temporary.replace(DATA)
    for kind, _, error in results:
        print(kind + ': ' + ('retained previous guides; ' + error if error else 'refreshed'))
    print(str(len(data['guides'])) + ' guide links available')


if __name__ == '__main__':
    main()
