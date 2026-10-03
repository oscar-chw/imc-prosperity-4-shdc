# IMC Prosperity 4: Team SHDC, a lessons-learned write-up

**904th of 18,803 teams (top 4.81%), 18th in Hong Kong; algorithmic 917th, manual 1,132nd** ([Results](#results)).

The field's best ideas set against ours, round by round, with the failure mechanisms studied afterwards. What the team built:

<!-- built:start -->
- **Tutorial:** fixed-fair-value (10,000) market making with inventory skew on EMERALDS; mean-reverting market making on TOMATOES.
- **Round 1:** fixed-fair-value takes plus passive quotes on OSMIUM; an online drift-slope estimate with drift-aware buys on PEPPER_ROOT.
- **Round 2:** wall-mid, inventory-neutral market making; a GP-UCB script that proposed the next parameter run.
- **Round 3:** market making on HYDROGEL, VELVETFRUIT and ten vouchers; buy-at-zero deep strikes; delta hedging costed and rejected.
- **Round 4:** fixed-anchor market making plus named-counterparty signals; a Kalman drift filter with an uncertainty gate.
- **Round 5:** Kalman/OU market making on 9 of 50 products; a gated one-lot cross-family residual trade.
<!-- built:end -->

![Our approach against the top teams', by product type: same idea, partly or late, different, field split, or not in our records](assets/strategy-map.png)

```bash
git clone <this repo> && cd imc-prosperity-4-shdc
bash scripts/demo.sh    # checks every link and round document, prints the results (Python 3, no installs)
```

Scores come from withheld leaderboard screenshots and strategies from a relayed AI audit of the team's unpublished code ([Limits](#limits)); the write-up was drafted with AI coding agents under Oscar's design and review.

## The problem

IMC Prosperity 4 is a team trading competition run by IMC Trading; the organiser reports [18,803 participating teams](https://prosperity.imc.com/). After a tutorial round there are five rounds. Each round has two independent tracks:

- **Algorithmic:** a Python `Trader` class that the platform runs against simulated market bots, under per-product position limits. New products arrive each round.
- **Manual:** a one-shot puzzle (an auction, an allocation game, a bidding game, an options portfolio, a news portfolio) answered by submitting numbers.

Several top-team write-ups describe rounds 1 and 2 as "phase 1" and rounds 3 to 5 as "phase 2", and appear to reset the leaderboard between them ([reference table](docs/top-teams-comparison.md#how-the-rounds-were-scored)).

## Approach

The team built one trader per round. Each row condenses its round document, which follows one template: products, our hypothesis, strategy, result, mistakes, and what top teams did. "Ours" is the audit of the team's code (Codex, 2026), relayed; "top teams" are public write-ups, placements as each states them ([credits](docs/credits.md)). A lesson marked DRAFT is a candidate drawn from the records, not Oscar's wording.

| Round | Products | Our strategy | Top-team strategy | Mistake or lesson |
|---|---|---|---|---|
| [Tutorial](docs/rounds/tutorial.md) | EMERALDS, TOMATOES | Fixed value 10,000 with inventory-skewed quotes; mean-reverting market making | The same fixed-value answer; [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) also pinned down the matching rules | DRAFT: nothing recorded shows we measured the matching rules before the scored rounds |
| [1](docs/rounds/round-1.md) | ASH_COATED_OSMIUM, INTARIAN_PEPPER_ROOT | Fixed-value takes plus passive quotes; online drift slope, capped sells | Wall-mid fair value; quote wide into an empty book side; buy PEPPER_ROOT to the limit early and hold ([Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4), 4th) | The team's notes warn the local replay may overstate. DRAFT: a replay is a filter, not a forecast |
| [2](docs/rounds/round-2.md) | Same two, plus a market-access bid | Wall mid, inventory-neutral; seven research methods, deployment unknown; GP-UCB proposals | Recurring bot takers at the same time, side and size across days ([Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4)) | DRAFT: their edge came from reading raw trades day against day, not from adding models |
| [3](docs/rounds/round-3.md) | HYDROGEL_PACK, VELVETFRUIT_EXTRACT, 10 call vouchers | Market making with a take overlay; filtered fair value; voucher quotes; delta hedge costed and rejected | Split: delta-hedged ([JaneRT](https://github.com/heyman7913/imc-prosperity-4), 19th), delta-adjusted quotes ([Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup), 57th); a fitted smile ([DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4), 28th) | DRAFT: cost a hedge before adding it, and record the inputs so the call can be re-checked (ours were not) |
| [4](docs/rounds/round-4.md) | Same, plus named counterparties | Fixed-anchor market making plus Marks 14, 38, 01, 55; Kalman drift sign with a t-statistic gate | Most shipped no counterparty signal; Marks 14 and 38 overfitted in three-day validation ([Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup)); regime detectors | We traded the two signals another team measured as overfitted. DRAFT: validate a counterparty signal across days before trading it |
| [5](docs/rounds/round-5.md) | 50 products in 10 families | Kalman/OU market making on 9 primary products; gated one-lot cross-family residual | Market-make all 50 as a backbone; PEBBLES prices sum to about 50,000; fade round-hundred jumps; cross-family baskets collapsed out of sample | Backtest PnL decayed across visible days, and the submitted file is not identified. DRAFT: record exactly which file was submitted |

The manual rounds are in [manual-rounds.md](docs/manual-rounds.md); the theme-by-theme comparison behind the figure is [top-teams-comparison.md](docs/top-teams-comparison.md).

## Results

**Official (final leaderboard).** Source: leaderboard screenshots, read 2026-06-01; images withheld pending permission.

<!-- results:start -->
| Track | Score | Global rank | Top % of 18,803 | Hong Kong rank |
|---|---:|---:|---:|---:|
| Overall | 233,959 | 904 | 4.81% | 18 |
| Algorithmic | 86,750 | 917 | 4.88% | 20 |
| Manual | 147,209 | 1,132 | 6.02% | 26 |
<!-- results:end -->

"Top %" is rank ÷ 18,803. The two tracks sum to the total: 86,750 + 147,209 = 233,959. Manual earned more points, but algorithmic ranked better against the field (917th against 1,132nd). Points are only comparable within a track, so the ranks are the fairer comparison. No per-round score or rank is recorded, and whether 233,959 covers both phases is still open ([pending](#pending-oscars-input)).

**LOCAL BACKTEST, NOT OFFICIAL.** The team's own replays, as the audit records them. They are not comparable with the official numbers above: they replay the visible sample days through a local matching model rather than the official run, and the audit does not say whether the round-5 figures are totals or per-day values.

| Round | What was replayed | Local result | Caveat recorded |
|---|---|---:|---|
| 1 | Round-1 trader, 3 days | ≈63,464 (3-day mean) | The team's FINDINGS.md warns that the 10k-tick replay may overstate |
| 5 | Cross-family gate, passive execution, visible days 2–4 | 127,494 | PnL decays across the days; hidden-test risk stated |
| 5 | Cross-family gate, take-only execution, visible days 2–4 | 165,281 | Same |

Source: audit of the team's code (Codex, 2026), relayed; original files not published.

## How to run

The demo needs only Python 3 (standard library) and finishes in seconds:

```bash
bash scripts/demo.sh     # link and round-template checks, then the result table and per-round summary
bash scripts/check.sh    # unit tests of the checker, then the demo (what CI runs)
```

To redraw the figure: `python scripts/make_figure.py` with any Python that has matplotlib. Its rows restate the docs, with the source file named on each row.

Five-minute reading path:

1. **[Results](#results)** (1 min): the score, and why the ranks matter more than the points.
2. **[top-teams-comparison.md](docs/top-teams-comparison.md)** (1 min): what the top teams did that we did not.
3. **[round-3.md](docs/rounds/round-3.md)** and **[round-5.md](docs/rounds/round-5.md)** (2 min): the delta-hedging decision, and the round with the most code and the clearest backtest warning.
4. **[lessons.md](docs/lessons.md)** (1 min): candidate lessons, each with its evidence.

Then, if there is time: [after-the-competition.md](docs/after-the-competition.md) (later, SYNTHETIC experiments on two failure mechanisms), [manual-rounds.md](docs/manual-rounds.md), [imc3-reference.md](docs/imc3-reference.md) and [credits.md](docs/credits.md).

## Architecture

The team's tooling and workflow, as far as the audit and Oscar's own account describe them:

```text
  round data ──► ROUND_N/analysis/*.py ──► ROUND_N/trader.py ──► Rust backtester ──► run log
                  (research scripts,          (the Trader)          (local replay)        │
                   parameter proposals)              ▲                                    ▼
                                                     └──── results/*.md decisions ◄── visualiser
```

This drawing is a reading of the folder layout, not a recorded process.

- **Folder layout** (per the audit): one `ROUND_N/` folder per round holding `trader.py` and `analysis/*.py`, decision documents under `results/`, and candidate files under `submissions/`.
- **Backtester:** GeyzsoN's Rust backtester for local replays ([credits](docs/credits.md)).
- **Visualiser and log reading:** gsgill7's fork of jmerle's Prosperity visualiser, which loads a run's log and plots prices, positions and PnL ([credits](docs/credits.md)). The audit records no separate team log parser.
- **Team interface:** in Oscar's words, "we also made interface for data analysis and visualisation". Its source has not been recovered.
- **Parameter proposals:** a GP-UCB script in round 2 (`ROUND_2/analysis/run_analysis.py:405-519`) suggested the next parameter pair to try; see [round 2](docs/rounds/round-2.md).

### Design decisions and trade-offs

Four decisions the audit records, each with the location it gives in the unpublished team files. The alternative each one gave up is stated, and so is what the records do not say.

- **Delta hedging rejected after costing it** (`ROUND_3/trader.py`; the audit gives no line range). Hedging the voucher book in VELVETFRUIT would have earned gamma-scalp value but paid the spread on every rebalance and used position limit. The modelled cost was higher, so the book stayed unhedged. Trade-off: lower trading cost for open exposure to VELVETFRUIT moves. The cost inputs are not recorded, and top teams split on the same call ([round 3](docs/rounds/round-3.md#the-delta-hedging-decision)).
- **A Kalman filter replaced a 5,000-tick drift gate** (`ROUND_4/trader.py:3-27`). The window cost O(5k) work per tick; a local-linear-trend Kalman filter costs O(1) and also reports the slope's uncertainty, so a t-statistic gate uses the drift sign only when it is clearly away from zero. Trade-off: no window to rescan, at the price of noise settings that must be chosen (the audit gives neither them nor the threshold) ([round 4](docs/rounds/round-4.md#from-a-5000-tick-gate-to-a-kalman-filter)).
- **A one-lot cross-family gate in round 5** (`ROUND_5/trader.py:53-78,88-150,390-466`; `results/R5_THESIS_STRATEGY_DECISION.md:21-33,56-62`). A residual trade across all 50 products fires only after warm-up, score, z-gap and spread gates, and never for more than one lot. Trade-off: a small, bounded bet on an idea other teams saw collapse out of sample, instead of either skipping it or sizing it up; market making stayed on 9 primary products rather than all 50 ([round 5](docs/rounds/round-5.md#strategy)).
- **A local replay that may overstate** (the team's FINDINGS.md, no line range given; the round-5 decision document above). The team kept a fast local replay as its filter and wrote down that it may overstate (round 1) and that its PnL decayed across visible days 2–4 (round 5). Trade-off: quick iteration against an optimistic number; no recorded go or no-go rule turned the warnings into a decision ([lessons](docs/lessons.md#process)).

This repository itself:

```text
README.md                       this page
docs/rounds/                    tutorial and rounds 1-5, one template each
docs/manual-rounds.md           the five manual challenges
docs/top-teams-comparison.md    what top teams did that we did not
docs/lessons.md                 candidate lessons with evidence
docs/after-the-competition.md   later SYNTHETIC studies of two failure mechanisms
docs/imc3-reference.md          Prosperity 3 write-ups, learning reference only
docs/credits.md                 tools and write-ups credited
assets/strategy-map.png         the figure above, drawn by scripts/make_figure.py
assets/README.md                why there are no screenshots yet
scripts/docs.py                 link and round-template checks; prints the summary
scripts/demo.sh                 the reading demo
scripts/check.sh                unit tests plus the demo; run by .github/workflows/ci.yml
tests/test_docs.py              each check shown to fail on a broken fixture
```

## Limits

- **No official per-round scores or ranks.** Only the final totals above are recorded. Round documents say so in their "Result" section.
- **Individual authorship is unknown.** The team folder has no git history, so nothing here attributes a strategy to one person. All strategies are the team's.
- **The code is not published.** It sits on a team machine and has not been through an authorship or release review. Everything about it here is second-hand: an AI audit, relayed.
- **Screenshots are withheld** until Oscar decides ([assets/README.md](assets/README.md)).
- **The round-5 submitted file is not identified.** The decision document names `submissions/r5_portfolio_cross_gate_v01.py`, which differs from the root `trader.py`.
- **Local backtests are not official** and, by the team's own notes, may overstate.
- **Top-team numbers are as each source states.** They were summarised from fetched pages and have not been re-checked line by line against those pages.
- **The post-competition experiments are SYNTHETIC.** No team data, fills or code went through them ([after-the-competition.md](docs/after-the-competition.md)).

### Pending Oscar's input

Open questions whose answers belong in this README; the round documents carry the per-round versions.

- Results: TODO-OSCAR: Q1 — does 233,959 cover all five rounds, or only rounds 3 to 5 after the reset? Is any per-round score or rank still visible?
- Authorship and permissions: TODO-OSCAR: Q3 — how many were on the team, which part was Oscar's, may teammates be named, and may the seven leaderboard screenshots be published?
- Code: TODO-OSCAR: Q5 — do the submitted trader files or the round logs still exist (team PC, the Prosperity portal's submission history, a team chat)?
- Lessons: Q4 is in [What I learned](#what-i-learned), where its answer goes.

## What I learned

TODO-OSCAR: Q4 — what was the costliest mistake, what is the biggest lesson, and what is the first thing to change for Prosperity 5?

Candidate lessons drawn only from the records and the audit. None of them is Oscar's own wording yet; [lessons.md](docs/lessons.md) gives the evidence for each.

1. **Make the per-tick update constant-time.** In round 4 the team replaced a drift gate that looked back over 5,000 ticks with a local-linear-trend Kalman filter (constant work per tick) plus a t-statistic gate on the estimated drift.

   DRAFT — Oscar to confirm
2. **Cost a hedge before adding it.** In round 3 the team rejected delta hedging on the vouchers because the modelled cost of hedging exceeded the modelled gamma-scalp value.

   DRAFT — Oscar to confirm
3. **A local replay is a filter, not a forecast.** The team's own notes say the round-1 replay may overstate, and the round-5 backtest PnL decayed across the visible days with a stated hidden-test risk.

   DRAFT — Oscar to confirm
4. **Record exactly which file was submitted.** For round 5 the decision document and the root trader disagree, and the records cannot settle which one ran.

   DRAFT — Oscar to confirm
