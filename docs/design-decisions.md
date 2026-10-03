# Design decisions and trade-offs

Four decisions the audit of the team's code (Codex, 2026), relayed, records. The first was the teammates' (round 3), the second and third Oscar's (rounds 4 and 5). What each gave up is stated, and so is what the records do not say.

## Delta hedging costed and rejected (round 3)

The audit records that the modelled cost of hedging the vouchers' delta in VELVETFRUIT exceeded the modelled gamma-scalp value. That comparison holds if the voucher book was long gamma; market making can leave it short, and the book's direction is not recorded. If it was short gamma, the question is cost against lower variance, not against profit. The cost inputs are not recorded either ([round 3](rounds/round-3.md#the-delta-hedging-decision)).

## A Kalman filter replaced a 5,000-tick drift gate (round 4)

The gain is the uncertainty: a local-linear-trend Kalman filter returns the slope with its variance, so a t-statistic gate uses the drift sign only when the slope is clearly away from zero. It also updates in constant time per tick, as a rolling-window slope with running sums could. The cost is noise settings to choose; the audit gives neither them nor the threshold ([round 4](rounds/round-4.md#from-a-5000-tick-gate-to-a-kalman-filter)).

## A one-lot cross-family gate (round 5)

A residual trade across all 50 products fires only after warm-up, score, z-gap and spread gates, and never for more than one lot: a small, bounded bet on a class of idea other teams saw collapse out of sample, while market making stayed on 9 primary products rather than all 50 ([round 5](rounds/round-5.md#strategy)).

## A fast local replay as the filter

The team iterated against local replays and wrote down that they may overstate (round 1) and decayed across visible days (round 5). No recorded go or no-go rule turned those warnings into a decision ([lessons](lessons.md#process)).
