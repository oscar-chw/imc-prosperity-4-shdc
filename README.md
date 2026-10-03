# IMC Prosperity 4: Team SHDC, a lessons-learned write-up

**904th of 18,803 teams (top 4.81%), 18th in Hong Kong; algorithmic 917th, manual 1,132nd** ([Results](#results)).

The field's best ideas set against ours, round by round, with the failure mechanisms studied afterwards. A team of three: teammates coded the early rounds; Oscar coded rounds 4 and 5 and verified the team's results ([who did what](#who-did-what)). What the team built:

<!-- built:start -->
- **Tutorial:** fixed-fair-value (10,000) market making with inventory skew on EMERALDS; mean-reverting market making on TOMATOES.
- **Round 1:** fixed-fair-value takes plus passive quotes on OSMIUM; an online drift-slope estimate with drift-aware buys on PEPPER_ROOT.
- **Round 2:** wall-mid, inventory-neutral market making; a GP-UCB script that proposed the next parameter run.
- **Round 3:** market making on HYDROGEL, VELVETFRUIT and ten vouchers; buy-at-zero deep strikes; delta hedging costed and rejected.
- **Round 4 (Oscar):** fixed-anchor market making plus named-counterparty signals; a Kalman drift filter with an uncertainty gate.
- **Round 5 (Oscar):** Kalman/OU market making on 9 of 50 products; a gated one-lot cross-family residual trade.
<!-- built:end -->

![Our approach against the top teams', by product type: same idea, partly or late, different, or not in our records](assets/strategy-map.png)

This repository is documentation; its demo verifies the write-up's links and structure and prints the summary (Python 3, no installs):

```bash
git clone <this repo> && cd imc-prosperity-4-shdc
bash scripts/demo.sh
```

Scores come from leaderboard screenshots (to be added) and strategies from a relayed AI audit of the team's unpublished code ([Limits](#limits)); the write-up was drafted with AI coding agents under Oscar's design and review.

## The problem

IMC Prosperity 4 is a team trading competition run by IMC Trading; the organiser reports [18,803 participating teams](https://prosperity.imc.com/). After a tutorial round there are five rounds (one `ROUND_N` folder each in the team's code, and five in every write-up), each with two independent tracks:

- **Algorithmic:** a Python `Trader` class that the platform runs against simulated market bots, under per-product position limits. New products arrive each round.
- **Manual:** a one-shot puzzle (an auction, an allocation game, a bidding game, an options portfolio, a news portfolio) answered by submitting numbers.

Several top-team write-ups describe rounds 1 and 2 as "phase 1" and rounds 3 to 5 as "phase 2", with separate phase totals ([scoring notes](docs/top-teams-comparison.md#how-the-rounds-were-scored)).

## Approach

One trader per round; what each ran is listed above. Each round document follows one template: products, our hypothesis, strategy, result, mistakes, and what top teams did. The table names the largest recorded difference from the top teams and a lesson derived from the records (not Oscar's words; his are under [What I learned](#what-i-learned)). The theme-by-theme detail is in [top-teams-comparison.md](docs/top-teams-comparison.md).

| Round | Products | Where top teams differed | Mistake or lesson (derived) |
|---|---|---|---|
| [Tutorial](docs/rounds/tutorial.md) | EMERALDS, TOMATOES | One team first tested the matching rules (no queue priority at the best price) | Nothing recorded shows we measured the matching rules before the scored rounds |
| [1](docs/rounds/round-1.md) | ASH_COATED_OSMIUM, INTARIAN_PEPPER_ROOT | Wall-mid fair value from the start; quoting wide into an empty book side; PEPPER_ROOT bought to the limit early and held | The team's notes warn the local replay may overstate. Lesson: a replay is a filter, not a forecast |
| [2](docs/rounds/round-2.md) | Same two, plus a market-access bid | Recurring bot takers found by comparing raw trades day against day | Compare raw trades day against day before adding models |
| [3](docs/rounds/round-3.md) | HYDROGEL_PACK, VELVETFRUIT_EXTRACT, 10 call vouchers | The write-ups that discuss a voucher delta hedge favour it; some fitted a volatility smile | Cost a hedge before adding it, and record the inputs so the call can be re-checked (ours were not) |
| [4](docs/rounds/round-4.md) | Same, plus named counterparties | Most shipped no counterparty signal; one team found copying Marks 14 and 38 did not generalise to a held-out day | We traded Marks 14 and 38. Lesson: validate a counterparty signal on a held-out day before trading it |
| [5](docs/rounds/round-5.md) | 50 products in 10 families | Market making on all 50; exact identities and round-hundred reversion; cross-family baskets dropped after failing out of sample | Backtest PnL decayed across visible days, and the submitted file is not identified. Lesson: record exactly which file was submitted |

The manual rounds are in [manual-rounds.md](docs/manual-rounds.md).

### Who did what

By Oscar's account (the team folder has no git history, so nothing else settles it): the team had three members. The two teammates, who stay anonymous, coded the tutorial and rounds 1 to 3. Oscar coded the final two rounds: in round 4, the Kalman drift gate that replaced the 5,000-tick gate, and the counterparty signals; in round 5, the Kalman/OU/inventory market making on nine primary products and the family cross-gate. In his words, "I even verified all their results".

## Results

**Official (final leaderboard).** Source: leaderboard screenshots, read 2026-06-01; images to be added.

<!-- results:start -->
| Track | Score | Global rank | Top % of 18,803 | Hong Kong rank |
|---|---:|---:|---:|---:|
| Overall | 233,959 | 904 | 4.81% | 18 |
| Algorithmic | 86,750 | 917 | 4.88% | 20 |
| Manual | 147,209 | 1,132 | 6.02% | 26 |
<!-- results:end -->

"Top %" is rank ÷ 18,803, and 86,750 + 147,209 = 233,959. Manual earned more points, but algorithmic ranked better (917th against 1,132nd); points are only comparable within a track. 233,959 and 904th are the final result; per-round scores were not recorded.

**LOCAL BACKTEST, NOT OFFICIAL.** The team's own replays of visible sample days through a local matching model, as the audit records them:

| Round | What was replayed | Local result | Caveat recorded |
|---|---|---:|---|
| 1 | Round-1 trader, 3 days | ≈63,464 (3-day mean) | The team's notes warn that the 10k-tick replay may overstate |
| 5 | Cross-family gate, passive execution, visible days 2–4 | 127,494 | PnL decays across the days; hidden-test risk stated |
| 5 | Cross-family gate, take-only execution, visible days 2–4 | 165,281 | Same |

Source: audit of the team's code (Codex, 2026), relayed.

**Replay against result.** The local round-5 replay of one component, the cross-family gate, showed 127,494 to 165,281 on three visible days. That is more than the team's official algorithmic score for the whole competition, 86,750. The two are not directly comparable: whether the local figures are totals or per-day values is not recorded, the replay uses a local matching model, and it covers visible days, not the hidden test. It is not a measured overstatement. It is the plainest sign in the records that a replay's level is a filter, not a forecast ([lessons](docs/lessons.md#process)).

## How to run

Python 3 standard library only; both finish in seconds:

```bash
bash scripts/demo.sh     # link and round-template checks, then the result table and per-round summary
bash scripts/check.sh    # unit tests of the checker, then the demo (what CI runs)
```

The figure is redrawn by `python scripts/make_figure.py` with any Python that has matplotlib; each row names the document it restates.

Five-minute reading path: [Results](#results) (1 min), [top-teams-comparison.md](docs/top-teams-comparison.md) (1 min), [round-3.md](docs/rounds/round-3.md) and [round-5.md](docs/rounds/round-5.md) (2 min: the hedging decision and the clearest backtest warning), [lessons.md](docs/lessons.md) (1 min). Then [after-the-competition.md](docs/after-the-competition.md) (later SYNTHETIC experiments), [manual-rounds.md](docs/manual-rounds.md), [imc3-reference.md](docs/imc3-reference.md) and [credits.md](docs/credits.md).

## Architecture

The team's tools, per the audit: GeyzsoN's Rust backtester for local replays, gsgill7's fork of jmerle's Prosperity visualiser for reading run logs ([credits](docs/credits.md)), and, in Oscar's words, "we also made interface for data analysis and visualisation" (source not recovered). The code was organised one folder per round, with decision documents alongside.

This repository:

```text
README.md                       this page
docs/rounds/                    tutorial and rounds 1-5, one template each
docs/top-teams-comparison.md    what top teams did that we did not, by theme
docs/lessons.md                 candidate lessons with evidence
docs/manual-rounds.md           the five manual challenges
docs/after-the-competition.md   later SYNTHETIC studies of two failure mechanisms
docs/imc3-reference.md, credits.md
assets/strategy-map.png         the figure above, drawn by scripts/make_figure.py
scripts/docs.py                 link and round-template checks; prints the summary
scripts/demo.sh, check.sh       the demo; tests plus demo (run by .github/workflows/ci.yml)
tests/test_docs.py              each check shown to fail on a broken fixture
```

### Design decisions and trade-offs

Four decisions the audit records in the team's code; the first was the teammates', the second and third Oscar's. What each gave up is stated, and so is what the records do not say.

- **Delta hedging costed and rejected (round 3).** The audit records that the modelled cost of hedging the vouchers' delta in VELVETFRUIT exceeded the modelled gamma-scalp value. That comparison holds if the voucher book was long gamma; market making can leave it short, and the book's direction is not recorded. If it was short gamma, the question is cost against lower variance, not against profit. The cost inputs are not recorded either ([round 3](docs/rounds/round-3.md#the-delta-hedging-decision)).
- **A Kalman filter replaced a 5,000-tick drift gate (round 4).** The gain is the uncertainty: a local-linear-trend Kalman filter returns the slope with its variance, so a t-statistic gate uses the drift sign only when the slope is clearly away from zero. It also updates in constant time per tick, as a rolling-window slope with running sums could. The cost is noise settings to choose; the audit gives neither them nor the threshold ([round 4](docs/rounds/round-4.md#from-a-5000-tick-gate-to-a-kalman-filter)).
- **A one-lot cross-family gate (round 5).** A residual trade across all 50 products fires only after warm-up, score, z-gap and spread gates, and never for more than one lot: a small, bounded bet on a class of idea other teams saw collapse out of sample, while market making stayed on 9 primary products rather than all 50 ([round 5](docs/rounds/round-5.md#strategy)).
- **A fast local replay as the filter.** The team iterated against local replays and wrote down that they may overstate (round 1) and decayed across visible days (round 5). No recorded go or no-go rule turned those warnings into a decision ([Results](#results)).

## Limits

- **Second-hand, unpublished code.** Every strategy fact is an AI audit of the team's files, relayed. The audit cites per-round `trader.py` files, analysis scripts and decision documents with line ranges; none is published, so this repository does not repeat those pointers. Who coded which round rests on Oscar's account.
- **No official per-round scores or ranks**, and the round-5 submitted file is not identified (the decision document and the root trader differ).
- **Local backtests are not official** and, by the team's own notes, may overstate.
- **Top-team figures** were re-checked against each write-up's README on 2026-10-03 through a fetch tool that quotes the page; figures it could not find were removed. Placements are as each source states them. The Prosperity 3 notes in [imc3-reference.md](docs/imc3-reference.md) were not re-checked.
- **Screenshots** may be published but are not here yet ([assets/README.md](assets/README.md)). **The post-competition experiments are SYNTHETIC** ([after-the-competition.md](docs/after-the-competition.md)).

### Pending Oscar's input

- Code: TODO-OSCAR: optional: excerpts of the team's trader files once they are recovered from the team PC. Non-blocking.
- Screenshots: permitted with the team name visible; pending transfer ([assets/README.md](assets/README.md)).

## What I learned

In Oscar's words:

> Our direction was right, but our execution wasn't. We needed more execution experience, and honestly I didn't know quant well enough then. For example, we found correlations, but I didn't truly understand what pair trading means and got it wrong.

The first thing to change for Prosperity 5:

> Learn the finance fundamentals first.

### The costliest mistake, derived from the records

Derived by this write-up from the audit and the round-5 decision document, not stated by Oscar, and its cost is not measured: **shipping the round-5 cross-family gate on a replay that was already warning.**

- The round-5 decision document chose the cross-gate submission while recording that its local PnL decayed across visible days 2–4 and naming the risk that the hidden test days behave differently ([round 5](docs/rounds/round-5.md#mistakes)).
- That replay put one component at 127,494 to 165,281, above the team's official algorithmic score for the whole competition, 86,750 ([Results](#results)); the round-1 notes had already warned that the local replay may overstate.
- No go or no-go rule turned the warnings into a decision, and which file was finally submitted cannot now be settled.

The cross-family residual gate is also the records' closest match to the correlation-based trade in Oscar's lesson. That link is this write-up's inference, not his statement. Further lessons derived from the records are in [lessons.md](docs/lessons.md).

### What I'd do with pair trading now (learned after the competition)

Post-competition learning, not what the team did:

1. **Test the spread, not the correlation.** Two prices can be highly correlated while their spread wanders off for good. Test whether the spread is stationary: the Engle–Granger two-step (regress one price on the other, then an ADF test on the residuals, using Engle–Granger rather than standard ADF critical values), or Johansen's test for three or more series.
2. **Estimate the hedge ratio.** OLS of one price on the other gives β, but depends on which is the dependent variable; total least squares treats both alike; a Kalman filter gives a time-varying β when the relationship drifts.
3. **Measure the speed of reversion.** Fit an AR(1), s(t) = c + φ·s(t−1) + ε, to the spread; the OU rate is κ = −ln φ per step and the half-life is ln 2 / κ. A half-life longer than the trading horizon rules the pair out.
4. **Trade the z-score, with stops.** Enter when the spread's z-score, on a lookback of a few half-lives, passes a threshold; exit near zero; stop out when the z-score keeps widening, a trade outlives several half-lives, or a rolling cointegration test fails (a structural break).
5. **Validate out of sample, net of costs.** Select pairs and fit parameters on one period, trade on another, and count every pair screened: among many random series some will look cointegrated by chance.

References: R. F. Engle and C. W. J. Granger, "Co-integration and error correction: representation, estimation, and testing", *Econometrica* 55(2), 1987; G. Vidyamurthy, *Pairs Trading: Quantitative Methods and Analysis*, Wiley, 2004.
