# Lessons

Three kinds of lesson, kept apart:

1. **Oscar's own lesson**, in his words, is in the README's [What I learned](../README.md#what-i-learned) section.
2. **Derived from the records.** Drawn by this write-up (AI-assisted) only from the audit of the team's code (Codex, 2026), relayed, and from the final scores. They are not Oscar's words, and each cites its evidence.
3. **Lessons other teams wrote down.** Theirs, summarised and credited. Our records can test some of them and not others.

## Derived from the records

### Process

**A local replay is a filter, not a forecast.** The team's own notes warn that the round-1 replay over 10k ticks may overstate its ≈63,464 three-day mean. In round 5 the backtest PnL decayed across visible days 2–4, and the decision document wrote down the hidden-test risk ([round 5](rounds/round-5.md)). The plainest sign is a level: the round-5 cross-gate portfolio replay (local) gave 127,494 (passive) to 165,281 (take-only) on visible days 2–4, more than the team's official algorithmic score of 86,750 for the scored rounds (very likely rounds 3 to 5, per the [README](../README.md#results)). That is not a measured overstatement: whether the local figures are totals or per-day values is not recorded, and the replay saw visible days through a local matching model, not the hidden test days. Both warnings were recorded; what is not recorded is a rule that turned them into a go or no-go.

**Record exactly which file was submitted.** The round-5 decision document names `submissions/r5_portfolio_cross_gate_v01.py`; the root `ROUND_5/trader.py` is a different file. With no git history, nobody can now say which one ran, so the round-5 result cannot be tied to its code.

**Compare the two tracks by rank, not points.** Manual earned 147,209 points to algorithmic's 86,750, yet ranked 1,132nd against 917th. Reading the points alone gives the wrong answer about where the team stood against the field.

### Modelling

**Gate a signal on its uncertainty, not only its sign.** In round 4 a drift gate over a 5,000-tick window became a local-linear-trend Kalman filter, whose slope estimate comes with a variance, plus a t-statistic gate, so the drift sign is used only when the estimate is clearly away from zero ([round 4](rounds/round-4.md)). The filter also updates in constant time per tick, but that is secondary: a rolling-window slope can too, with running sums.

**Cost a hedge before adding it, and keep the inputs.** In round 3 the team modelled the cost of delta-hedging the vouchers against the gamma-scalp value it would earn, found the cost higher, and left the book unhedged ([round 3](rounds/round-3.md#the-delta-hedging-decision)). That comparison holds for a long-gamma book; the book's direction, like the cost inputs, is not recorded. The two top-team write-ups that discuss a voucher hedge both favour it.

**Use a Bayesian optimiser as a proposal tool when data is scarce.** In round 2, GP-UCB fitted to 3 backtest results proposed the next pair of `PASSIVE_CAP` and `CLEAR_OFFSET` to try, rather than claiming an optimum ([round 2](rounds/round-2.md)).

## Lessons other teams wrote down

| Lesson | Who stated it | Can our records test it? |
|---|---|---|
| The backtester is a filter, not ground truth; fit on two days and test on the third | [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) | Partly: our round-1 and round-5 warnings agree with it |
| Ship only if the worst single backtest day is positive | [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) | No per-day figures recorded |
| A threshold should sit in a stable region, not on a spike; random series give many chance "cointegrated" pairs | [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) | Our cross-family gate is the kind of idea it warns about |
| Statistical significance at p < 0.05 is not enough when testing many ideas; edge must survive costs | [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) | Our round-2 research, several methods with none known to have shipped, is the setting it describes |
| Simple broad market making beat elaborate relative value | [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) | We market-made 9 of 50 round-5 products |
| Add per-product PnL attribution early | [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) | Not recorded |
| Write the change list down before opening a new day of data; re-run sweeps after every baseline change | [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) | Our `results/*.md` decision documents are related; whether change lists came first is not recorded |
| Re-check the environment every round instead of carrying beliefs across rounds; a human and an AI converging on a wrong belief entrench it | [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) | Not recorded |
| Solve for the crowd first in manual rounds | [JaneRT](https://github.com/heyman7913/imc-prosperity-4) | No manual records |
| Do not hard-code estimator seeds calibrated on sample data; let them warm up on live data | [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) | Our round-5 gate has a warm-up period; its length is not recorded |
