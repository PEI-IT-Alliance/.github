# Launch checklist (go live today)

## 1. Push the repo (10 min)
- [ ] Create a public repo named `.github` in PEI-IT-Alliance. No README, no license.
- [ ] Push this folder to `main`.
- [ ] Run `scripts/fetch-assets.sh`, add the five remaining logos, commit.

## 2. Check the page (5 min)
- [ ] Open github.com/PEI-IT-Alliance signed out. The profile shows.
- [ ] Toggle dark mode. Logos stay visible.
- [ ] Check on a phone. Cards stack cleanly.

## 3. Org settings (10 min)
- [ ] Verify peiitalliance.com under org settings, verified domains. Adds the Verified badge.
- [ ] Update the org description: "The nonprofit tech community for PEI and Atlantic Canada."
- [ ] Pin the `.github` repo on the org overview.

## 4. Staff team and review (10 min)
- [ ] Create team `staff` and add Alliance staff.
- [ ] Give `staff` write access to `.github`.

## 5. Protect main (10 min)
- [ ] Generate a key pair: `ssh-keygen -t ed25519 -f profile_bot -N ""`
- [ ] Add `profile_bot.pub` as a deploy key on `.github` with write access.
- [ ] Add the private key as repo secret `PROFILE_DEPLOY_KEY`.
- [ ] Create a branch ruleset on `main`: require a pull request, one approval, review from code owners, block force pushes.
- [ ] Add "Deploy keys" to the ruleset bypass list. The daily bot pushes through, people go through review.
- [ ] Run the workflow by hand from the Actions tab. Confirm a green run.
- [ ] Delete the local key files.

## 6. After launch
- [ ] Ship `/feed.json` on the website (see `docs/feed-spec.md`). Until then, the README shows friendly fallback links.
- [ ] Measure: in site analytics, filter `utm_source=github` for event signups. Track org followers monthly.
- [ ] Announce on LinkedIn and in Slack.
