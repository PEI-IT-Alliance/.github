#!/usr/bin/env bash
# Pulls the homepage hero and the PEI Devs logo from the live site.
# Drop the other five program logos into profile/assets/logos/ by hand.
set -euo pipefail
cd "$(dirname "$0")/.."

curl -fL "https://www.peiitalliance.com/images/site/hero-home.png" -o profile/assets/hero.png
echo "Saved hero.png ($(du -h profile/assets/hero.png | cut -f1)). Aim for under 500 KB."

echo "Program logos still needed (SVG preferred):"
for f in the-foundry foundry-residency the-night-shift ai-together tech-week-pei pei-devs; do
  if [ -f "profile/assets/logos/$f.svg" ]; then echo "  ✓ $f.svg"; else echo "  ✗ $f.svg"; fi
done
echo "PEI Devs PNG from the site, if you lack an SVG:"
echo "  https://www.peiitalliance.com/assets/partners/pei-devs.png"
