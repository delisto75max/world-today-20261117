# world-today-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/delisto75max/world-today-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/delisto75max/world-today-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page that sums up the world news of **Tuesday 17 November 2026**: the Kerch Bridge strike as the lead, the alleged Washington "dirty bomb" plot and the market slide as second and third stories, four illustrated stories from Manila, the West Bank, Washington's AI-chip rules and Japan's airspace, a world map with five labelled markers, a figures panel, and a nine-item "also reported" band — sixteen stories in all, with the date repeated in the masthead, the date band, the map stamp and the footer.

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

- `0–160` masthead, world edition line, and the date band `TUESDAY · 17 NOVEMBER 2026`
- `168–412` lead: Kerch Bridge crippled, with the bridge illustration
- `416–636` world map with five labelled markers, and the day in numbers
- `644–730` the "dirty bomb" plot claim and the market slide
- `738–920` Manila protests, settler attack, AI-chip curbs, Japan jets scrambled
- `928–1024` figures, nine also-reported stories and sources

Body type stays at 14 px and above in the briefs band, item headlines at 22 px, the lead at 54 px; the page is built to stay legible at 300 px across.

## Sources

Guardian, AP, Reuters, CNN, Al Jazeera, Euronews, NPR, Anadolu, DW, Times of Israel, Democracy Now — reporting of 17 November 2026. Contested claims are labelled as claims (`Reported Washington target; Tehran denies`; `Moscow says it downed 1,400 drones`).

## License

MIT — see `LICENSE`.
