# Round 4

Sources: audit of the team's code (Codex, 2026), relayed; original files not published. Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-4-exotic-options).

**Who:** Oscar coded this round (his account).

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

The earlier gate judged drift over a 5,000-tick window. The team replaced it with a local-linear-trend Kalman filter, which tracks two hidden numbers, the price level and its slope, and updates both from each new price.

What the filter adds is the slope's **uncertainty**: alongside the estimate it returns a variance. The team gated on the t-statistic, the slope divided by its standard error, so the drift sign is used only when the estimate is clearly away from zero. A bare drift estimate gives no such test.

The filter also updates in constant time per tick. That is a secondary gain: as implemented, the window cost work in proportion to its length, but a rolling-window slope can be kept in constant time with running sums. The audit gives neither the gate threshold nor the filter's noise settings.

## Result

- Official: per-round scores were not recorded; only the final result is.
- No local backtest figure is recorded for this round.

## Mistakes

The records show none for this round. Another team (Team Ryan Challman) found that copying Mark 14 and Mark 38 did not generalise to a held-out day (below); our HYDROGEL logic used both. Whether that cost us anything is not recorded.

Oscar's own account of this round is not recorded beyond his overall lesson in the [README](../../README.md#what-i-learned).

## What top teams did

- **Most judged the named counterparties too weak to trade.** [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (4th, as stated) put no Mark-based strategy in its final submission. [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) (2nd, phase 2) found nothing they used.
- **A few names had partial support.** [JaneRT](https://github.com/heyman7913/imc-prosperity-4) (19th) found that after Mark 67 bought, the price was higher 50 ticks later 58.8% of the time. [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) (93rd) bucketed the bots' trades by distance from an EMA fair value and found Mark 14 and Mark 55 better in different regions, Mark 55 especially consistent. [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) found a clear edge only in Mark 67, too small to beat their round-3 algorithm after transaction costs.
- **Copying Mark 14 and Mark 38 did not generalise.** [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) (57th) fitted per-trader weights on the training days; on the held-out day the weights did not generalise. Disabling the two biases recovered about 15.8k of held-out PnL, and shortening a VFE reset window added about 7.8k more.
- **Regime detection.** [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) (28th) added a three-state detector (pinned, trending, noisy) after their fixed peg broke in round 3. JaneRT classified regimes from the opening price, and list hard-coding the three regime centres to the observed opens as their round-4 mistake; a Gaussian mixture fitted to more opens would have been more robust.
- **Threshold search.** Une Baguette Fromage simulated future VFE paths from their Ornstein–Uhlenbeck model to set round-4 thresholds.

The comparison: our Kalman drift filter with an uncertainty gate answers the same question as DTU's and JaneRT's regime detectors (is the price trending right now?), with an explicit uncertainty test. Our use of Marks 14 and 38 is the choice Team Ryan Challman measured as not generalising, though Dark Forest Hunter rated Mark 14 well in some regions.
