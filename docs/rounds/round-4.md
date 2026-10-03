# Round 4

Sources: audit of the team's code (Codex, 2026), relayed; original files not published (`ROUND_4/trader.py:3-27`). Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-4-exotic-options).

## Products

The round-3 products (HYDROGEL_PACK, VELVETFRUIT_EXTRACT and the ten vouchers), plus one new kind of data: the trade tape now names the counterparty on each trade ("Mark 01", "Mark 14" and so on). One write-up ([Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup)) reports a strong down-drift of about 65 ticks on the third sample day.

## Our hypothesis

The records hold the strategy, not the reasoning. The strategy implies: some named counterparties trade with information, so following them adds edge; and VFE's short-term drift can be estimated well enough to filter those signals.

## Strategy

From the audit:

- **HYDROGEL_PACK:** market making around a fixed anchor, plus signals from named counterparties Mark 14, Mark 38, Mark 01 and Mark 55.
- **VELVETFRUIT_EXTRACT:** a target position taken from counterparty behaviour, kept only when it agrees with the sign of the drift estimated by a Kalman filter. A mark-to-market stop-out and end-of-day controls limit the damage when it is wrong.
- **Vouchers:** the audit does not record round-4 voucher logic.

### From a 5,000-tick gate to a Kalman filter

The earlier drift gate looked back over 5,000 ticks, so each update cost work in proportion to the window: O(5k) per tick. The team replaced it with a local-linear-trend Kalman filter. That model tracks two hidden numbers, the price level and its slope, and updates both from each new price with a fixed amount of arithmetic: O(1) per tick, with no window to store or rescan.

The filter also returns how uncertain its slope estimate is. The team added a gate on the t-statistic, the slope divided by its standard error, so the drift sign is used only when the estimate is clearly away from zero. The audit does not give the threshold or the filter's noise settings.

## Result

- Official: no per-round score is recorded.

  TODO-OSCAR: Q1 — round-4 algorithmic score and rank, if the Prosperity portal still shows them.
- No local backtest figure is recorded for this round.

## Mistakes

The records show none for this round. Two other teams found that copying Mark 14 and Mark 38 overfitted (below); our HYDROGEL logic used both. Whether that cost us anything is not recorded.

TODO-OSCAR: Q4 — what went wrong in round 4, and did the counterparty signals earn or lose?

## What top teams did

- **Most judged the named counterparties too weak to trade.** [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (4th, as stated) shipped none. [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) (2nd, phase 2) found little in them.
- **Two names had partial support.** [JaneRT](https://github.com/heyman7913/imc-prosperity-4) (19th) found that after Mark 67 bought, the price was higher 50 ticks later 58.8% of the time. [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) (93rd) grouped the bots by how far their trades sat from fair value and found Mark 55 the one consistently good trader. [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) found an edge only in Mark 67, and it did not survive trading costs.
- **Mark 14 and Mark 38 overfitted.** [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) (57th) validated across the three sample days and found that copying them did not hold up: removing the named-trader bias recovered about 15.8k in their tests, and shortening a reset window recovered about 7.8k more.
- **Regime detection.** [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) (28th) added a three-state detector (pinned, trending, noisy) after their fixed peg broke in round 3. JaneRT used a Gaussian mixture on opening prices, and list hard-coded regime centres as their round-4 mistake.
- **Threshold search.** Une Baguette Fromage tuned their round-4 trade thresholds by Monte Carlo simulation.

The comparison: our Kalman drift filter with an uncertainty gate answers the same question as DTU's and JaneRT's regime detectors (is the price trending right now?), and it is cheaper per tick than the window it replaced. Our use of Marks 14 and 38 is the choice two other teams measured as overfitting.
