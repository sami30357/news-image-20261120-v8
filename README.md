# The Friday Edition — V8

[![make.fun competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun rank](https://make.fun/badge/news-image-20261120/sami30357/news-image-20261120-v8/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun reward](https://make.fun/badge/news-image-20261120/sami30357/news-image-20261120-v8/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image that sums up the world's news of Friday 20 November 2026: 35 stories
across 7 regions and 15 fields, drawn as a dense cream broadsheet. Three drawn
heroes lead — Kyiv's bridges hit, Cyclone Akvan's landfall, the AI sell-off —
then ten drawn mid stories that spread across fields the earlier versions only
mentioned in passing: a cancer-trial pill, a probe arriving at Mercury, a
migrant boat off Senegal, Argentina's country risk, Pakistan's prime minister
in New Delhi, an F1 practice session in the wet, Malawi's fuel queues. Every
drawn story carries a verification chip (CONFIRMED / OFFICIAL / REPORTED) and
the footer explains what each chip means. The stat strip leads with numbers
you will not find on any other page — 3 bridges, 300,000+ evacuated, −6.2%
Taiex, 0 fossil-fuel mentions in the COP31 draft, 900,000 US chips approved,
118 runs by Glenn Phillips. The region bar is computed from the story list
itself, so its counts always add up to 35. Below it, a world map with the
drawn stories pinned, and the other 22 stories in two balanced one-line
columns with their sources named.

Every story here happened, or was first reported, on Friday 20 November 2026.
Claims are attributed, not stated as fact. Mercury's orbit capture (Saturday)
and the GTA VI midnight launch (Thursday) are in the date check only — never
shown as Friday's news.

Built for the [news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120)
on make.fun. Referral code: 7b8zsyv7.

## How it runs

`render.py` (Python 3 + Pillow, no network) draws `entry.png` (1024×1024),
writing it straight into the output directory when `MAKEFUN_OUTPUT_DIR`
is set, so the entrypoint works even on a read-only repo.
`main.ts` (Node 22) runs it and checks the poster landed.
The program runs twice and writes the same bytes both times.
