# world-today-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/delisto75max/world-today-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/delisto75max/world-today-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page that sums up the world news of **Tuesday 17 November 2026**: the date as the page's headline, three illustrated leads (the Kerch Bridge span collapse, Iran's drone strike on a US radar in Bahrain, the Quad summit in Manila), four more illustrated stories (US AI-chip curbs, the market slide, the West Bank killing, Japan's jet scramble), a world map with five labelled markers, a figures strip, and thirty-three one-line briefs from every region — forty stories in all.

Everything in the image is drawn by `render.py` with Pillow: flat vector shapes only, no photographs, no outlet logos, no third-party artwork. The world map uses Natural Earth 110m land (public domain), committed here as GeoJSON.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` checks the committed `entry.png` against the competition's limits (PNG signature, IHDR size, 1 MiB ceiling, IEND present) and copies it to `/output/entry.png` byte for byte, so two runs write identical files.

## Rebuild the image

```sh
python3 -m pip install Pillow
python3 render.py entry.png
```

## Layout

- `0–92` kicker line and the date headline `Tuesday 17 November 2026`
- `100–322` three illustrated leads, each with a kicker, headline and deck
- `330–514` four illustrated second stories
- `524–812` world map with five labelled markers, and thirty-three numbered briefs in three columns
- `826–900` figures strip
- `940–1024` attribution, sources and the date again

Cards keep their own illustration block; the briefs stay on one line each. The page is built so the date, the three leads and every card headline read at 300 px across.

## Sources

Guardian, AP, Reuters, CNN, Al Jazeera, Euronews, NPR, Anadolu, DW, Times of Israel, Democracy Now — reporting of 17 November 2026. Contested claims are labelled as claims (`Reported Washington target; Tehran denies`; `Moscow says it downed 1,400 drones`).

## License

MIT — see `LICENSE`.
