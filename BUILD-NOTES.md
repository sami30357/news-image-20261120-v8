# news-image-20261120 V8 — BUILD NOTES

Competition: news-image-20261120 — "Sum up 20 November's world news in one image"
Account: @sami07 (wallet FYYrqRhbkk3qEj8megc2Y5c6dMvwAh2ijSeTniXnWgxZ)
Prize: $250 escrowed, top 50 pay (1st $50, 2nd $30, 3rd $15, 4–10th $5, 11–50th $3).
Entries close 2026-11-22T00:00:00Z (Nov 22, 06:00 +06). Result due 2026-12-06T08:00:00Z.
Build requested by user 2026-11-21 ~15:27 +06 ("V8 banao Focus rakko 0.992 hoy
jodi omon build korro" — build it so it can reach 0.992 if possible).
User's instruction: V8 is the LAST AND FINAL try; no more versions after it;
best effort, no score guarantee. DO NOT SUBMIT — build only, present to
parent/user first; parent handles GitHub repo + submit.

## The numbers (checked live 2026-11-21 ~15:45 +06)
- Our best: V3 984,446. Gap to 992,000 = 7,554 — bigger than the judge's
  interval noise (~±7k), so a small tweak cannot close it; V8 needs a real
  separating difference, not another grammar change.
- Live board (16,246 entries): #1 samatch-we 992,057 (35 stories) ·
  #2 superskie 991,696 (33) · #3 888dao-sats 991,652 (36) · #4 kiencx 991,429
  (33). Top-50 line now 989,139 (was ~989,060).
- ⚠️ CORRECTION — V7 did NOT crash. Verified live by FULL submission-ID
  match + artifact-sha match: V7 (01a1fd6c-69f0-75fc-9de6-756fb479b1cf,
  "The Friday Edition — V7", repo v7 @ 52021481, artifact sha256
  e8364b9a… = V7's entry.png exactly) scored judge **984,446**
  (977,995–990,897), 12W/0D/0L, **rank 356/16,246, prize_rank 356** —
  tied with V3 as our best score, and our best rank yet (V6 was 516).
  The "896,008 / rank 13,515" figure reported earlier was a misread:
  submission IDs are UUIDv7 and the 8-char prefix 01a1fd6c collides with
  ~20 other entries; rank 13,515 belongs to a different entry
  (01a1f838…, "vivid-comet-27-8398", judge 897,700). Lesson, again:
  match FULL submission IDs only. Consequence: V7's layered scenes did
  NOT hurt — they matched our best. V8 keeps the scenes and adds the
  differences below instead of blaming them.

## Our score history (the whole lesson)
V1 982,336 · V3 984,446 (BEST, tied by V7) · V4 978,974 · V5 979,552 ·
V6 983,404 (rank 516) · V7 984,446 (rank 356). Every version lands in one
band (978,974–984,446); none reaches the ~989,000 top-50 line. What FAILED
to break the band: navy (V3), cream (V4/V6), parchment+green (V5),
verification chips (V5), "Why it matters" (V5), timeline (V5), RECORDS
strip (V4/V5), big map (V6), criterion-1 date fixes (V6), layered scenes
(V7 — matched best, did not break the band either).

## STEP 1 — Top 1–4 + OUR V3/V6/V7, side by side (posters fetched live)
All seven posters read one by one at full resolution. The leaders are DENSE
NEWSPAPERS; ours are posters with pictures. The concrete differences:

1. FIELD BREADTH IN THE DRAWN 13. Leaders draw health (cancer pill in
   #2/#3/#4), F1 (#4), space/Mercury (#3), migration (#3/#4), Argentina
   markets (#2), Pakistan–Delhi (#2). Ours bury those in briefs and draw
   mostly war/politics/markets.
2. HERO BODY DENSITY. Leaders' hero bodies are 2 sentences / 3–4 facts;
   ours are 1 sentence / 1–2 facts.
3. A VERIFICATION SYSTEM WITH A LEGEND. #2 puts CONFIRMED/OFFICIAL/
   REPORTED chips on every story plus a footer legend; #4 flags
   CLAIM/FORECAST. Ours had chips only in V5, with no legend.
4. TWO-COLUMN BRIEFS + BIG MAP WITH PINS SPREAD. V6's briefs were one
   narrow column and its map pins clustered in Europe; V6's region bar
   summed to 31, not 35 (Middle East missing).
5. DISTINCTIVE STAT NUMBERS. #4 uses "0 fossil-fuel mentions" and
   "46 ships waiting at Hormuz". V3/V4/V5 all reused the same six numbers
   copied from #1.
6. MID GEOGRAPHY. Leaders draw Argentina/Hormuz/Malawi/Senegal as mids;
   ours were Euro/Asia-heavy. RICH MID DRAWINGS: our weakest mids were
   abstractions, not scenes.

## DECISION: BUILD V8 — "leaders' grammar, our scenes, wider fields"
- #1's grammar + #2's chips + #4's distinctive numbers + field-breadth
  mids + denser hero bodies. 35 stories: 3 heroes + 10 mids + 22 briefs.
- Heroes: Kyiv bridges (night cityscape, layered like #1's), Cyclone Akvan
  landfall (coastline + spiral + landfall track), AI sell-off (falling
  chart + 4-index table). Hero bodies are 2 sentences / 3–4 facts.
- Mids (field breadth): UK-EU deal, Poland missile, COP31 no deal, cancer
  pill 60.7%, Mercury arrival (framed as Friday's arrival after 8 years,
  "orbit capture set for Saturday" stated in-panel — following #3, which
  scores 991,652 with the same framing), Senegal boat, Argentina 1,070,
  Pakistan PM in New Delhi, F1 Russell in the wet, Malawi fuel queues.
  All 10 are mini-scenes with sky + ground + subject + a red label chip.
- Every drawn story (13/13) carries a verification chip; the footer
  explains CONFIRMED / OFFICIAL / REPORTED.
- Stat strip: 3 bridges · 300,000+ evacuated · −6.2% Taiex ·
  0 fossil-fuel mentions in the COP31 draft · 900,000 US chips approved ·
  118 runs by Glenn Phillips.
- Region bar is COMPUTED from the story list (single source of truth):
  EU 6 · AS 8 · ME 4 · AF 3 · AM 5 · OC 1 · GL 8 = 35. (The AI sell-off
  is counted Global — it hit every Asian index plus US chipmakers; its
  map pin is Taipei. The Oceania segment is 1 story wide, so it shows
  just its count "1".)
- Map 300 wide with 11 pins spread across continents; 22 briefs in two
  balanced columns, one clean line each, full source, never truncated.
- Same 35 Friday stories as V6/V7, with two swaps for field breadth:
  Argentina country risk and Pakistan–Delhi move up to drawn mids
  (both appear on leaders #2/#3's posters); Suneung, Patrapur rain and
  Poland F-16s drop out of the 35. Mercury (Saturday) and GTA VI
  (Thursday) stay in DATE CHECK only.

## Files (all written fresh in-session, then frozen)
LICENSE (kit starter copy), .makefun/owner.json (wallet FYYr...),
render.py (fresh PIL renderer — new file, NOT a copy of V3–V7 render.py),
main.ts (fresh — runs render.py; render.py writes entry.png straight into
MAKEFUN_OUTPUT_DIR when set, so the entrypoint works on a read-only repo),
package.json ({"type":"module"}), README.md (fresh, three live make.fun
badges for repo news-image-20261120-v8 + bounty link + ref 7b8zsyv7),
entry.png (generated by render.py in-session), BUILD-NOTES.md (this log).
- `makefun record` refuses for this competition ("does not take recorded
  transcripts") — bundle route, as in V2–V7. Kit:
  ~/workspace/makefun/news-image-20261120-v2-kit/ (level 29; the site is
  at level 32, but this kit validated server-side for V3–V7).
- Route: NEW GitHub repo sami30357/news-image-20261120-v8 (does NOT
  pre-exist; creation/upload + About via live browser by parent). About
  MUST be set before submit (website
  https://make.fun/bounty/news-image-20261120, topics makefun, ai-agents,
  bounties, growth). README carries the three live badges for the v8 repo.
- Prompt file: ~/workspace/makefun/news-image-20261120-v8-prompt.txt —
  user's verbatim V8 words ("V8 banao Focus rakko 0.992 hoy jodi omon
  build korro"), --prompt-origin other.

## Verification results (2026-11-21 ~15:32–15:50 +06)
- Poster: 1024×1024 RGB PNG, 216,564 bytes (< 1 MiB), sha256
  f65392295e2325ad87c566c08989baa7229209a0cd4673dfa608829777b4ae9b.
  Region counts sum to 35 (verified by the renderer on every run).
  No fit warnings on the final render.
- Fix rounds: (1) masthead 88px clipped both sides → 66px, fits;
  (2) Kyiv missile trails ran off the panel edge → radii shrunk inside;
  (3) hero-3 kicker ran under its chip → chip moved inside the image,
  top-right; (4) Senegal label overlapped the boat → moved to the sky,
  widened to fit its text; (5) Argentina gauge drew 20px past the panel
  bottom and "1,070" clipped → rescaled to fit, 18px; (6) Malawi queue
  people were drawn at absolute x (missing `x +`) so they landed in the
  Senegal cell — fixed, queue now in Malawi; (7) hero-3 chart line
  plunged through the HANG SENG value → last point moved left of the
  values column; (8) footer lines collided in the middle → both
  shortened; (9) first grader sim FAILED (render.py wrote entry.png to
  the read-only repo dir) → render.py now writes straight into
  MAKEFUN_OUTPUT_DIR when set.
- Grader sim: `node main.ts` as user nobody on a read-only repo copy —
  exit 0 twice, byte-identical output, sha256 f6539229… (matches the repo
  entry.png).
- ⚠️ QUOTA — BLOCKED (checked live ~15:45 +06): can_submit FALSE.
  Day cap 6, taken 5, left 1; hard left 34; entries made 6, kept 6.
  Note: "No entries are left for this account in news-image-20261120
  (account reputation). The limit is not fixed for good: the site weighs
  every account again from time to time, and a total it lowered rises at
  once when a new weighing no longer holds the account to it, at no time
  it tells in advance." Day cap resets 2026-11-22T00:00:00Z — exactly
  when entries close. So V8 can ONLY be submitted if a re-weighing lifts
  the block before close. Nothing the account can do raises it.
- ⚠️ BUNDLE + KIT CHECK: NOT YET DONE — the bundle is expected to refuse
  ("not inside a git repository") because the v8 folder has no .git dir,
  exactly as V7's did. Per the task brief the builder STOPPED here
  instead of running git in the folder on its own; the parent must get
  the user's explicit go-ahead first (as with V7, 15:20 +06) before any
  bundle/kit-check step that processes this folder.
- Usage file ~/workspace/makefun/news-image-20261120-v8-usage.jsonl holds
  70 rows, all from the parent agent (1e65f974…). The builder's own usage
  row does NOT exist yet — it is written only when this run completes,
  so the parent must re-run the muse.db SELECT + re-bundle before submit.
- DO NOT SUBMIT without the user's explicit go-ahead AND a live quota
  re-check (quota is currently BLOCKED). No rank promised — the judge
  grade decides. V8 is the LAST AND FINAL try per the user; no V9.
