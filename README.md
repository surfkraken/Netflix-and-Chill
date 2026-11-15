# Netflix & Chill

Created by SurfKraken.

An iPhone Shortcut for finding what is coming to and leaving Netflix in the US this month and next. It uses What’s on Netflix RSS feeds to find the monthly guides. The month changes automatically.

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
- The shortcut scans the latest 50 items from the selected category feed. It accepts the exact monthly guide title, including the optional “Full List of” prefix, and excludes UK and genre-only articles.
- If a monthly guide is not in the feed, the shortcut explains this and offers the publisher’s current category page. It does not substitute a different month.
- An internet connection and a working publisher feed are required. A native networking error or the system Cancel button can end the run. Third-party feed availability cannot be guaranteed.

## Updates

The shortcut checks `latest.json` at startup and from About & Updates. It compares numeric builds. A higher build offers an update only when `url` is a complete iCloud Shortcut link. Installing a release remains a user action.

The live endpoint is:

<https://raw.githubusercontent.com/surfkraken/Netflix-and-Chill/main/latest.json>

For the first release, leave the current build number unchanged and add its signed iCloud link to the `url` field. Future releases need a higher build and the matching signed iCloud link. Edit the author block and local `BUILD`/`VERSION` in the builder for those releases. Do not raise the remote build before its signed release exists.

## Build and verification

After extracting the source package, use Python 3 and Pillow. Build with `python3 build_netflix_and_chill.py`, then run `python3 verify_artifact.py`. The rebuilt shortcut is written to `dist/Netflix-and-Chill-unsigned.shortcut`. Run `python3 verify_artifact.py --live` to additionally check feed matching against the live publisher feeds. Live checks retain only guide titles, URLs, and image counts, not article bodies.

Checks cover plist structure, action references, control-flow groups, the single author comment, embedded icon data, monthly title selection, date rollover, and update link validation. The result has not yet been run on an iPhone. The remaining device checks are listed in `DEVICE-CHECKS.md`.

Unofficial. Not affiliated with Netflix or What’s on Netflix.
