[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/cryptotainment/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/cryptotainment/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125 — The World in One Image

A 1024×1024 newspaper front page summing up world news of
**Wednesday 25 November 2026**:

- **Lead:** Ukraine hits Russian ships at sea — Zelenskyy confirms drone
  strikes in the Gulf of Finland and off Libya; Putin vows retaliation.
- **Middle East:** Houthis strike Riyadh's tallest tower; 11 wounded.
- **United States:** Huawei convicted in a U.S. criminal trial over its
  Iran business.
- **Washington:** Trump pardons the Thanksgiving turkeys "Freedom" and
  "Feathers".
- **Asia:** a 5.6-magnitude quake shakes Nepal's Koshi Province.
- **Also today:** International Day to End Violence Against Women.

## How it works

`render.py` (Pillow, run locally) draws the front page into `entry.png`.
`main.py` (Python 3.13, standard library only, no network) copies
`entry.png` to `/output/entry.png`, so both grader runs write
byte-identical output.

Run locally:

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see LICENSE.
