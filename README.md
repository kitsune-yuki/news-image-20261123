[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/kitsune-yuki/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/kitsune-yuki/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — 23 November 2026

A make.fun entry for ["Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123):
a modern newspaper front page with a pixel-art illustration, summing
up Monday 23 November 2026 in one picture.

## How this image was made

1. **Research the day's news** — the top stories of 23 November 2026:
   the widening Gulf war (Iran hits U.S. bases in Bahrain and tankers
   in the Strait of Hormuz), the COP31 climate talks collapsing in
   Antalya, Russian strikes on Ukraine, Gaza, the U.S. House result,
   plus Mexico, Indonesia and South Korea.
2. **Draw the illustration as pixel art** — `pixel.py` draws the
   burning tanker at dusk one pixel at a time on a tiny 234x48 grid
   (graded dusk sky, low sun, shaded containers, lit windows, layered
   fire, a thick smoke column drifting left, missile trails, a
   tugboat), then scales it up with NEAREST so every pixel stays
   crisp. It writes `scene.png` (936x192).
3. **Compose the front page** — `compose.py` (Pillow + DejaVu fonts)
   pastes the pixel-art scene into a modern newspaper layout: the
   masthead, the big date, the lead headline, four story panels and
   an "Also today" strip. It writes `entry.png` (1024x1024).
4. **Ship it** — `main.py` (Python 3.13, standard library only) copies
   `entry.png` to `/output/entry.png`. No network, no drawing at
   run time, so the entry is fully offline and deterministic.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Regenerate the image

```sh
python3 pixel.py && python3 compose.py
```
