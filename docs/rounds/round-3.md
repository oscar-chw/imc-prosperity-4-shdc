# Round 3

Sources: audit of the team's code (Codex, 2026), relayed; original files not published (`ROUND_3/trader.py`). Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-3-two-bid-game).

## Products

- **HYDROGEL_PACK:** a price near 9,990 with a spread of about 16.
- **VELVETFRUIT_EXTRACT** (VFE, limit 200): a price near 5,250.
- **Ten call vouchers on VFE**, VEV_4000 to VEV_6500 (limit 300 each): options with strikes from 4,000 to 6,500.

These facts are stated by two or more top-team write-ups (for example [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) and [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4)).

## Our hypothesis

The records hold the strategy and one recorded decision. The strategy implies: HYDROGEL can be market-made around a stable value with opportunistic takes; VFE's fair value is noisy and needs filtering; vouchers can be market-made; the two deepest out-of-the-money strikes are sometimes offered at zero, which is free optionality.

## Strategy

From the audit:

- **HYDROGEL_PACK:** market making plus a take overlay that crosses the spread when an order is mispriced.
- **VELVETFRUIT_EXTRACT:** a filtered fair value with quotes skewed by inventory.
- **Vouchers:** market making.
- **VEV_6000 and VEV_6500:** buy at a price of zero whenever offered and hold to the end of the day.
- **Delta hedging: considered and rejected.** The audit records an explicit decision: the modelled cost of hedging the vouchers' delta in VFE exceeded the modelled value of gamma scalping.

### The delta-hedging decision

A voucher book has delta: its value moves with VFE. Hedging means trading VFE against the vouchers so that the book is flat to small VFE moves. For a long-option book, rebalancing that hedge as VFE moves buys low and sells high: gamma scalping. It pays when VFE moves more than the vouchers' implied volatility prices in.

Every rebalance, though, crosses the VFE spread and uses VFE position limit. The team set the two against each other: the expected cost of rebalancing against the expected gamma-scalp gain. Cost was higher, so the book was left unhedged. That is a reasoned decision. Its inputs (spread, rebalance frequency, assumed volatility) and the size of the gap are not recorded, so it cannot be re-checked here.

## Result

- Official: no per-round score is recorded.

  TODO-OSCAR: Q1 — round-3 algorithmic score and rank, if the Prosperity portal still shows them.
- No local backtest figure is recorded for this round.

## Mistakes

The records show none for this round. Whether the HYDROGEL drift that hurt another team (below) also hit our quotes is not recorded.

TODO-OSCAR: Q4 — what went wrong in round 3, and was the unhedged voucher book a cost or a saving in hindsight?

## What top teams did

**On hedging, the field split.**

- [JaneRT](https://github.com/heyman7913/imc-prosperity-4) (19th, as stated) priced vouchers with Black–Scholes and delta-hedged them.
- [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) (57th) ran delta-adjusted market making in the vouchers. They also report that a voucher fair value anchored on Black–Scholes lost them about 64k per strike.
- [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (4th) found implied volatility stable per strike, so there was no smile to trade; they priced at average implied volatility and traded VFE itself with an Ornstein–Uhlenbeck fit and thresholds.
- [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) (583rd, the closest write-up to our rank) computed a delta hedge in round 4 but never switched it on, and list that as a mistake.

So our decision has company on both sides. Without the inputs to the team's cost model, which side was right for us stays open.

**On volatility.** [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) (28th) started with one flat volatility of 0.20 and later fitted a parabola to implied volatility across strikes. [JaneRT](https://github.com/heyman7913/imc-prosperity-4) list a flat volatility that missed the smile as their round-3 mistake.

**On the deep strikes.** Quoting VEV_6000 and VEV_6500 at a bid of 0 or 1 appears in several write-ups. In round 4, [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) noted one named counterparty (Mark 22) selling these strikes at 0. Our buy-at-zero rule matches this.

**On HYDROGEL.** DTU's fixed-peg market making broke on HYDROGEL when the price drifted about 70 ticks within a session; they fixed it in round 4 with a three-state regime detector (pinned, trending, noisy). [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) (2nd, phase 2) instead traded HYDROGEL and VFE mean reversion around fixed values with symmetric bands, for about +297,716 in this round.
