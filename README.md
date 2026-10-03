# IMC Prosperity 4: Team SHDC, a lessons-learned write-up

A record of how team SHDC played IMC Prosperity 4 (April 2026), what the strongest teams did that we did not, and what we would change. It is documentation, not a code dump: the team's trading code is not published (see [Limits](#limits)).

This write-up was drafted with AI coding agents under Oscar's design and review.

Two sources are cited throughout:

- **Scores and ranks:** leaderboard screenshots, read 2026-06-01; images withheld pending permission.
- **What the team ran:** audit of the team's code (Codex, 2026), relayed; original files not published. File and line references below (for example `ROUND_4/trader.py:3-27`) point into those unpublished files, as the audit gives them.

## The problem

IMC Prosperity 4 is a team trading competition run by IMC Trading; the organiser reports [18,803 participating teams](https://prosperity.imc.com/). After a tutorial round there are five rounds. Each round has two independent tracks:

- **Algorithmic:** a Python `Trader` class that the platform runs against simulated market bots, under per-product position limits. New products arrive each round.
- **Manual:** a one-shot puzzle (an auction, an allocation game, a bidding game, an options portfolio, a news portfolio) answered by submitting numbers.

Several top-team write-ups describe rounds 1 and 2 as "phase 1" and rounds 3 to 5 as "phase 2", and appear to reset the leaderboard between them ([reference table](docs/top-teams-comparison.md#how-the-rounds-were-scored)).

**Our result: 904th of 18,803 teams (top 4.81%), 18th in Hong Kong.**

| Track | Score | Global rank | Top % of 18,803 | Hong Kong rank |
|---|---:|---:|---:|---:|
| Overall | 233,959 | 904 | 4.81% | 18 |
| Algorithmic | 86,750 | 917 | 4.88% | 20 |
| Manual | 147,209 | 1,132 | 6.02% | 26 |

Source: leaderboard screenshots, read 2026-06-01; images withheld pending permission. "Top %" is rank ÷ 18,803. The two tracks sum to the total: 86,750 + 147,209 = 233,959.

Manual earned more points, but algorithmic ranked better against the field (917th against 1,132nd). Points are only comparable within a track, so the ranks are the fairer comparison.

## Approach

The team built one trader per round. The table is a summary of the audit; each round document follows the same template: products, our hypothesis, strategy, result, mistakes, and what top teams did.

| Round | Products | What the team ran | Detail |
|---|---|---|---|
| Tutorial | EMERALDS, TOMATOES | Fixed fair value 10,000 with inventory-skewed market making; mean-reverting market making | [tutorial](docs/rounds/tutorial.md) |
| 1 | ASH_COATED_OSMIUM, INTARIAN_PEPPER_ROOT | Fixed-fair-value takes plus passive quotes with inventory controls; an online drift-slope estimate for the drifting product | [round 1](docs/rounds/round-1.md) |
| 2 | same two | Wall-mid, inventory-neutral market making; a GP-UCB script that proposed the next parameter run | [round 2](docs/rounds/round-2.md) |
| 3 | HYDROGEL_PACK, VELVETFRUIT_EXTRACT, 10 call vouchers | Market making with a take overlay; filtered fair value with inventory skew; voucher market making; delta hedging costed and rejected | [round 3](docs/rounds/round-3.md) |
| 4 | same, plus named counterparties | Fixed-anchor market making plus counterparty signals; a Kalman drift filter with an uncertainty gate | [round 4](docs/rounds/round-4.md) |
| 5 | 50 products in 10 families | Kalman/OU/inventory market making on 9 primary products; a gated one-lot cross-family residual trade | [round 5](docs/rounds/round-5.md) |

The manual rounds are in [manual-rounds.md](docs/manual-rounds.md); the side-by-side with top teams is in [top-teams-comparison.md](docs/top-teams-comparison.md).

## Results

**Official (final leaderboard).** Source: leaderboard screenshots, read 2026-06-01; images withheld pending permission.

| Track | Score | Global rank | Top % of 18,803 | Hong Kong rank |
|---|---:|---:|---:|---:|
| Overall | 233,959 | 904 | 4.81% | 18 |
| Algorithmic | 86,750 | 917 | 4.88% | 20 |
| Manual | 147,209 | 1,132 | 6.02% | 26 |

TODO-OSCAR: Q1 — does 233,959 cover all five rounds, or only rounds 3 to 5 after the reset? Is any per-round score or rank still visible?

**LOCAL BACKTEST, NOT OFFICIAL.** The team's own replays, as the audit records them. They are not comparable with the official numbers above: they replay the visible sample days through a local matching model rather than the official run, and the audit does not say whether the round-5 figures are totals or per-day values.

| Round | What was replayed | Local result | Caveat recorded |
|---|---|---:|---|
| 1 | Round-1 trader, 3 days | ≈63,464 (3-day mean) | The team's FINDINGS.md warns that the 10k-tick replay may overstate |
| 5 | Cross-family gate, passive execution, visible days 2–4 | 127,494 | PnL decays across the days; hidden-test risk stated |
| 5 | Cross-family gate, take-only execution, visible days 2–4 | 165,281 | Same |

Source: audit of the team's code (Codex, 2026), relayed; original files not published.

## How to read this

Five minutes:

1. **Results** above (1 min): the score, and why the ranks matter more than the points.
2. **[top-teams-comparison.md](docs/top-teams-comparison.md)** (1 min): what the top teams did that we did not.
3. **[round-3.md](docs/rounds/round-3.md)** and **[round-5.md](docs/rounds/round-5.md)** (2 min): the delta-hedging decision, and the round with the most code and the clearest backtest warning.
4. **[lessons.md](docs/lessons.md)** (1 min): candidate lessons, each with its evidence.

Then, if there is time: [after-the-competition.md](docs/after-the-competition.md) (later, SYNTHETIC experiments on two failure mechanisms), [manual-rounds.md](docs/manual-rounds.md), [imc3-reference.md](docs/imc3-reference.md) and [credits.md](docs/credits.md).

To check this repo's internal links and round-document structure: `bash scripts/check.sh`.

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
assets/README.md                why there are no screenshots yet
scripts/check.sh                link and heading checks for this repo
```

## Limits

- **No official per-round scores or ranks.** Only the final totals above are recorded. Round documents say so in their "Result" section.
- **Individual authorship is unknown.** The team folder has no git history, so nothing here attributes a strategy to one person. All strategies are the team's.

  TODO-OSCAR: Q3 — how many were on the team, which part was Oscar's, may teammates be named, and may the seven leaderboard screenshots be published?
- **The code is not published.** It sits on a team machine and has not been through an authorship or release review. Everything about it here is second-hand: an AI audit, relayed.

  TODO-OSCAR: Q5 — do the submitted trader files or the round logs still exist (team PC, the Prosperity portal's submission history, a team chat)?
- **Screenshots are withheld** until Oscar decides ([assets/README.md](assets/README.md)).
- **The round-5 submitted file is not identified.** The decision document names `submissions/r5_portfolio_cross_gate_v01.py`, which differs from the root `trader.py`.
- **Local backtests are not official** and, by the team's own notes, may overstate.
- **Top-team numbers are as each source states.** They were summarised from fetched pages and have not been re-checked line by line against those pages.
- **The post-competition experiments are SYNTHETIC.** No team data, fills or code went through them ([after-the-competition.md](docs/after-the-competition.md)).

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
