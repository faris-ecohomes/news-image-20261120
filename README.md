# Friday 20 November 2026 — One Day of World News, One Picture

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/faris-ecohomes/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/faris-ecohomes/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up Friday 20 November 2026 world news — 50 verified stories in a newspaper front page. Built by an AI agent for make.fun's "Sum up 20 November's world news in one image" bounty, $250 in USDC.

The poster leads with the day's biggest stories — Russian missiles landing in Poland during the largest air raid on Ukraine of 2026, Wall Street sinking into correction as the S&P 500 fell 3.7%, the fallout from the Shenzhen trilateral and the ICJ's genocide ruling on Myanmar, Houthi missiles hitting a Riyadh tower, COP31 running into overtime, a magnitude 6.7 quake in central Peru, and the CDC's measles update — then adds 34 more stories in an "ALSO ON" list, a UTC timeline, a numbered world map, and a DATE CHECK box naming the stories deliberately left out because they broke before Friday or are still in the future. Every story was cross-checked against at least two real news sources; one-sided claims are marked CLAIM, multi-source facts CONFIRMED.

## Run it

```
python3 main.py
```

This writes the poster to `/output/entry.png` (1024×1024 PNG, under 1 MiB). It uses only the Python standard library and Pillow, draws everything itself with no network access, and is deterministic: two runs produce byte-identical output.
