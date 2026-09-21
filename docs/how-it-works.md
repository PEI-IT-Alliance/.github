# How the org profile works

This repository is `PEI-IT-Alliance/.github`. It does two jobs: it holds the page people
see at [github.com/PEI-IT-Alliance](https://github.com/PEI-IT-Alliance), and it holds the
community health files that every other repository in the org inherits when it has none
of its own.

## What the page is made of

`profile/README.md` is the page. GitHub renders that one file on the organization
overview. Everything in it is written by hand except two blocks, which a script rewrites.

| Section | Source |
|---|---|
| Hero image, headline, member counts | Hand-written |
| **Next up** | Rewritten from `https://www.peiitalliance.com/api/events` |
| Pick your program (six cards) | Hand-written, images in `profile/assets/cards/` |
| **From the Alliance** | Rewritten from `https://www.peiitalliance.com/api/news` |
| Thinking about PEI, Stay in touch | Hand-written |

The two live blocks are marked in the file:

```markdown
<!-- EVENTS:START -->
...anything here gets replaced...
<!-- EVENTS:END -->
```

`scripts/update_readme.py` only ever touches the text between a `START` and its matching
`END`. If a marker goes missing the script stops with an error rather than guessing, so
the page cannot be half-rewritten. Everything outside the markers is yours to edit by
pull request.

## How the page rebuilds

`.github/workflows/update-readme.yml` runs `scripts/update_readme.py` on a schedule:

1. **Daily at 10:00 UTC** (6 or 7 AM Atlantic, depending on daylight time). Also on
   demand from the Actions tab, and on any push that changes the script or the workflow
   itself.
2. The job checks out the repository over SSH using the `profile-bot` deploy key.
3. The script fetches both endpoints, renders the three soonest events and the three
   newest articles, and writes them into the marked blocks.
4. If `profile/README.md` changed, the job commits as `pei-it-alliance-bot` and pushes to
   `main`. If nothing changed, it prints `Nothing to commit.` and stops. Most days there
   is nothing to do.

Each source is fetched independently and neither can break the run. An endpoint that is
down, slow, malformed, or empty falls back to a friendly link:

> We're lining up the next few events. See the full calendar at peiitalliance.com/events.

The job exits green either way, so a bad morning at the API never turns into a red badge
or a blank section on the page.

### What the script does with each source

The two endpoints do not share a shape, so each has its own reader. See
[`content-sources.md`](content-sources.md) for the full payloads.

Events come back wrapped as `body.result`, with `name`, `url`, and `start.utc`. A start
is a real timestamp, so it is converted to Halifax time for display. Events already past
are dropped, and the three soonest are shown. Their URLs point at the ticketing host, so
they are left alone; UTM tags are only ever added to links on `peiitalliance.com`.

News comes back as a flat `articles` list, with `title`, `url`, and `publishedAt`. A
published date is stamped at midnight UTC rather than being a real timestamp, so it is
read as given. Converting it to Halifax time would roll every date back a day. Anything
from an earlier year shows its year, so a 2025 piece does not read as this February.

### Running it yourself

```bash
python scripts/update_readme.py
EVENTS_URL=file:///path/to/sample-events.json python scripts/update_readme.py
NEWS_URL=file:///path/to/sample-news.json python scripts/update_readme.py
```

It is safe to run twice. The second run reports `No changes.`

## The program cards

The six cards under "Pick your program" use screenshots of each program's own page,
because the programs have no logo files. The website brands them typographically, with a
letterspaced eyebrow above a display serif headline, so there is no mark to download.

Each card is 800x250, cropped to a 3.2:1 box around the wordmark and compressed with
`pngquant`. They live in `profile/assets/cards/` and are listed in
[`../profile/assets/ASSETS.md`](../profile/assets/ASSETS.md) with the page each came from
and the recipe for refreshing one. Because they are screenshots, they will drift as the
site is redesigned.

Cards carry their own background, so they read on both GitHub themes. A logo on a
transparent background often does not, which is why the one real logo we have,
`profile/assets/logos/pei-devs.png`, was recoloured onto transparency before being set
aside.

## How the bot is allowed to push

A branch ruleset on `main` would normally block a bot pushing directly. GitHub lets you
add **deploy keys** to a ruleset's bypass list, but not `GITHUB_TOKEN`, which is what a
workflow uses by default. So the workflow authenticates as a deploy key instead:

- `profile-bot` is an ed25519 deploy key on this repository with write access.
- Its private half is the repository secret `PROFILE_DEPLOY_KEY`.
- `actions/checkout` reads that secret through `ssh-key:` and clones over SSH.

The result is that the daily bot pushes straight through while people go through review.
If the secret is ever removed, checkout quietly falls back to `GITHUB_TOKEN`, which works
only while `main` is unprotected.

To rotate the key: generate a new pair, add the public half as a deploy key with write
access, replace the secret with the private half, delete the old key, then run the
workflow by hand to confirm it is still green.

## Editing the page

Anything outside the two marked blocks is a normal pull request. Worth knowing:

- Links to `peiitalliance.com` use the `www` subdomain and carry
  `?utm_source=github&utm_medium=org_profile&utm_campaign=readme`, so the site can
  attribute traffic from here.
- Images are referenced by absolute `raw.githubusercontent.com` URLs on `main`, because
  relative paths do not resolve on the org overview page.
- Check changes on both GitHub themes and at phone width. The pull request template
  covers this.

## Still outstanding

- [ ] Create the `staff` team and give it write access. `CODEOWNERS` assigns every file
      to `@PEI-IT-Alliance/staff`, and code-owner review cannot work until that team
      exists.
- [ ] Create the branch ruleset on `main`: require a pull request, one approval, review
      from code owners, block force pushes, and **add Deploy keys to the bypass list**.
      Without that last item the daily push starts failing.
- [ ] Watch one daily run that actually has something to commit. Every other link has
      been verified, but no bot push has happened yet.

The rest of the go-live checklist is in [`../LAUNCH.md`](../LAUNCH.md).
