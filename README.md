# PEI-IT-Alliance/.github

Org-wide defaults and the public profile for [PEI IT Alliance](https://www.peiitalliance.com).

| Path | Purpose |
|---|---|
| `profile/README.md` | The page people see at github.com/PEI-IT-Alliance |
| `profile/assets/` | Hero photo and program card images |
| `scripts/update_readme.py` | Pulls events from `/api/events` and news from the site feed |
| `.github/workflows/update-readme.yml` | Runs the script daily |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `.github/ISSUE_TEMPLATE/` | Defaults every org repo inherits unless it has its own |
| `docs/feed-spec.md` | The events API shape, and the `/feed.json` contract for news |
| `LAUNCH.md` | Go-live checklist |

The script only edits text between the `EVENTS` and `NEWS` markers. Edit everything else by pull request.

Test locally:

```bash
python scripts/update_readme.py
EVENTS_URL=file:///path/to/sample-events.json python scripts/update_readme.py
FEED_URL=file:///path/to/sample-feed.json python scripts/update_readme.py
```
