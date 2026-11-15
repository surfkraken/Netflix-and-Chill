# Netflix & Chill

Created by SurfKraken.

An iPhone Shortcut for finding what is coming to and leaving Netflix in the US this month and next. It reads an automatically maintained index of What’s on Netflix guides. The month changes automatically.

## The menu

| Item | What it opens |
| --- | --- |
| Coming This Month | This month’s arrivals guide |
| Last Call | This month’s departures guide |
| Next Month | Next month’s arrivals or departures |
| About & Updates | Author, source details, and a manual update check |
| Quit | Ends the shortcut |

The vCard menus include embedded icons and subtitles. They do not create or save contacts. Completed screens return to the main menu. Closing a monthly guide with Done returns to the shortcut.

The guide opens in an in-app Safari view with its original artwork and attribution. RSS has selected banners and stills, rather than individual posters for every title. This release opens the publisher’s guide; it does not build a separate menu of every show or movie.

## Installation

Download `Netflix-and-Chill-unsigned.shortcut` from this repository. Sign it with your usual shortcut signing workflow before importing it on an iPhone. It was assembled from native Shortcuts actions using the same action schemas as the author’s existing shortcuts.

The complete build source and verification results are in `Netflix-and-Chill-Source.zip`. Extract it to get the builder, verification script, documentation, and `dist` folder.

The first signed iCloud release link is pending. No iCloud installation link has been invented or substituted.

## Data and availability

- No paid API, AI service, Netflix credentials, or monthly edits are required.
- Guides cover Netflix US. Schedules can change, and the publisher may update a guide during the month.
- Departures can list the first day a title is unavailable. Watch before that date.
- The shortcut downloads a small JSON index from GitHub. It does not use the native RSS article parser or depend on exact headline punctuation.
- A GitHub Actions job refreshes the index from the publisher’s two RSS feeds every six hours. It identifies monthly US guides by their canonical links, and retains previously verified links when a feed fails.
- If a monthly guide is not in the index, the shortcut explains this and offers the publisher’s current category page. It does not substitute a different month.
- An internet connection is required. A native networking error or the system Cancel button can end the run. Scheduled refreshes can be delayed by GitHub; the publisher’s guides remain third-party content.

The index is `netflix-guides.json`. Its `fetched_at` fields show the most recent successful refresh for each feed. The workflow is `.github/workflows/refresh-guides.yml`, and its collector is `refresh_netflix_guides.py`. Neither requires API keys or monthly manual edits.

## Updates

The shortcut checks `latest.json` at startup and from About & Updates. It compares numeric builds. A higher build offers an update only when `url` is a complete iCloud Shortcut link. Installing a release remains a user action.

The live endpoint is:

<https://raw.githubusercontent.com/surfkraken/Netflix-and-Chill/main/latest.json>

Future releases need a higher build and the matching signed iCloud link. Edit the author block and local `BUILD`/`VERSION` in the builder for those releases. The builder writes `dist/release-manifest-pending.json`; promote it to `latest.json` only after its `url` contains the signed, device-tested release. Building a new unsigned file does not change the live release manifest.

## Build and verification

After extracting the source package, use Python 3 and Pillow. Refresh the source with `python3 refresh_netflix_guides.py`, build with `python3 build_netflix_and_chill.py`, then run `python3 verify_artifact.py`. The rebuilt shortcut is written to `dist/Netflix-and-Chill-unsigned.shortcut`. Run `python3 verify_artifact.py --live` to additionally verify the deployed JSON index. The index contains guide URLs and refresh metadata, not article bodies.

Checks cover plist structure, action references, control-flow groups, the single author comment, embedded icon data, monthly guide lookup through the emitted actions, retained data during feed failures, date rollover, and update link validation. The repair still needs an iPhone run. The remaining device checks are listed in `DEVICE-CHECKS.md`.

Unofficial. Not affiliated with Netflix or What’s on Netflix.
