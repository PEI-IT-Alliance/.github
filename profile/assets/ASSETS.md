# Assets

| File | Status | Notes |
|---|---|---|
| `hero.png` | In place | Homepage hero, 1280 px wide, 194 KB. Pulled with `scripts/fetch-assets.sh` and resized. |
| `logos/pei-devs.png` | In place | Teal wordmark on a transparent background, trimmed to 716x119. |
| `logos/the-foundry.svg` | Missing | |
| `logos/foundry-residency.svg` | Missing | |
| `logos/the-night-shift.svg` | Missing | |
| `logos/ai-together.svg` | Missing | |
| `logos/tech-week-pei.svg` | Missing | |

The five missing logos do not exist anywhere yet. The website brands those programs
typographically, with a letterspaced eyebrow and a display serif headline, so there is
nothing to download. Their cards in `profile/README.md` currently show the program name
as a heading and no image. Add the `<img>` tag back to a card once its logo exists.

Check every logo on GitHub's dark theme. A dark logo on a transparent background
disappears. Add a white stroke or a light variant if needed.

Using PNG instead of SVG? Keep the same name with `.png` and update the path in
`profile/README.md`.
