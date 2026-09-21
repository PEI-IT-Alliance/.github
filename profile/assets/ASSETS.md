# Assets

| File | Notes |
|---|---|
| `hero.png` | Homepage hero, 1280 px wide, 194 KB. Pulled with `scripts/fetch-assets.sh` and resized. |
| `cards/*.png` | Program card images. Screenshots of each program page, 800x250, about 30 KB each. |
| `logos/pei-devs.png` | The PEI Devs wordmark, teal on a transparent background. Not currently used in the README. |

## Program cards

The programs have no logo files. The website brands them typographically, with a
letterspaced eyebrow and a display serif headline, so each card in `profile/README.md`
uses a screenshot of the program's own page instead.

| Card | Source page |
|---|---|
| `cards/the-foundry.png` | https://www.peiitalliance.com/the-foundry |
| `cards/foundry-residency.png` | https://www.peiitalliance.com/the-foundry/residency |
| `cards/the-night-shift.png` | https://www.peiitalliance.com/the-night-shift |
| `cards/ai-together.png` | https://www.peiitalliance.com/ai-together |
| `cards/tech-week-pei.png` | https://www.peiitalliance.com/tech-week |
| `cards/pei-devs.png` | https://www.peiitalliance.com/pei-devs |

To refresh one: open the page at 1280x800, screenshot the hero, crop to a 3.2:1 box
around the wordmark, resize to 800x250, and run it through `pngquant --quality 60-88`.
Keep each card under about 50 KB.

Cards carry their own background, so they read on both GitHub themes. A logo on a
transparent background does not. Check every transparent asset against the dark theme
before shipping it.
