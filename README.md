# PEI-IT-Alliance/.github

Org-wide defaults and the public profile for [PEI IT Alliance](https://www.peiitalliance.com).

| Path | Purpose |
|---|---|
| `profile/README.md` | The page people see at github.com/PEI-IT-Alliance |
| `profile/assets/` | Hero photo and program card images |
| `scripts/update_readme.py` | Pulls events and news from the site API |
| `.github/workflows/update-readme.yml` | Runs the script daily |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `.github/ISSUE_TEMPLATE/` | Defaults every org repo inherits unless it has its own |
| `docs/content-sources.md` | The two API endpoints the script reads, and what it reads from each |
| `LAUNCH.md` | Go-live checklist |

The script only edits text between the `EVENTS` and `NEWS` markers. Edit everything else by pull request.

Test locally:

```bash
python scripts/update_readme.py
EVENTS_URL=file:///path/to/sample-events.json python scripts/update_readme.py
NEWS_URL=file:///path/to/sample-news.json python scripts/update_readme.py
```
