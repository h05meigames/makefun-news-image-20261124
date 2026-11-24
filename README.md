# The World — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/h05meigames/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/h05meigames/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-image summary of Tuesday 24 November 2026's world news, drawn as a
newspaper front page for the
[news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty on
[make.fun](https://make.fun/r/0ene8b3q).

## The day's news

- **Lead — Nvidia reinstates CEO Jensen Huang.** Days after his shock
  removal over an affair with an alleged spy, the board brings Huang back.
  Donald Trump says he brokered the return: "I made the deal."
- **Britain / Europe:** the UK and EU strike a "landmark" deal; Burnham
  says it could make the next decade "much better".
- **Gaza:** Israeli attacks have turned Gaza into a "toxic wasteland",
  Oxfam and the Conflict and Environment Observatory warn — air, soil and
  water dangerous for decades.
- **Indonesia:** the factory fire death toll rises to 24; rescuers still
  search for around 30 missing workers in Banten.
- **India / Nepal:** India pledges $1.6bn to Nepal; Modi and Nepal's PM
  Balendra Shah flag off the Saryu-Kamala Express in a reset of ties.
- **Manchester:** a US rapper postpones two Co-op Live arena shows after
  an unknown substance forces an evacuation.
- **Also today:** Carlos Alcaraz wins a maiden ATP Finals title; the World
  Chess Championship begins in Geneva; Max Verstappen wins the Las Vegas
  Grand Prix; the NHS launches the world's largest AI breast-cancer
  screening trial; Tyson Fury reveals a schizophrenia diagnosis;
  BepiColombo enters orbit around Mercury.

Sources: BBC, Reuters, The Times of India, Jagran Josh, Disclosure News —
all stories first reported 24 November 2026.

## How it works

`render_frontpage.py` draws the 1024×1024 front page with Pillow (no
network, no randomness — the same script always writes identical bytes).
`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`.

```sh
python3 render_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
