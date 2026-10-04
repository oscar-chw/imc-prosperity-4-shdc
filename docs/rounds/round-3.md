# Round 3

Sources: audit of the team's code (Codex, 2026), relayed; original files not published. Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-3-two-bid-game).

**Who:** teammates (anonymous) coded this round ([who did what](../../README.md#who-did-what)).

## Products

- **HYDROGEL_PACK:** a price near 9,990, with an average spread of about 16.
- **VELVETFRUIT_EXTRACT** (VFE): a price near 5,250.
- **Ten call vouchers on VFE**, VEV_4000 to VEV_6500: options with strikes from 4,000 to 6,500.

The fair values are as [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) state them, the HYDROGEL spread as [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) states it.

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

A voucher book has delta: its value moves with VFE. Hedging means trading VFE against the vouchers so that the book is flat to small VFE moves. Every rebalance crosses the VFE spread and uses VFE position limit.

What the hedge is worth depends on the book's direction, which is **not recorded**. Market making can leave the book long or short options.

- **If the book was long gamma**, rebalancing buys low and sells high (gamma scalping), which pays when VFE moves more than implied volatility prices in. The audit's comparison, modelled rebalancing cost against modelled gamma-scalp value, is the right one for this case, and on it the cost was higher.
- **If the book was short gamma**, rebalancing locks in losses as VFE moves; a hedge then buys lower variance, not profit, and the comparison would be cost against risk.

The audit phrases the decision in the first form. The inputs (spread, rebalance frequency, assumed volatility), the size of the gap and the book's direction are not recorded, so the decision cannot be re-checked here.

## Result

- Official: per-round scores were not recorded; only the final result is.
- No local backtest figure is recorded for this round.

## Mistakes

The records show none for this round. Whether the HYDROGEL drift that hurt another team (below) also hit our quotes is not recorded.

No first-hand account of this round is recorded: teammates coded it, and Oscar's overall lesson is in the [README](../../README.md#what-i-learned).

## What top teams did

**On hedging.**

- [JaneRT](https://github.com/heyman7913/imc-prosperity-4) (19th, as stated) priced vouchers with Black–Scholes and shorted VFE to keep net delta near zero.
- [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) (583rd, the closest write-up to our rank) computed the portfolio delta in round 4 but never passed it to their order logic, and list that as a mistake.
- [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (4th) found implied volatility almost constant per option through each day, so there was no smile to trade; they modelled VFE itself with an Ornstein–Uhlenbeck process.
- [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) (57th) report that a voucher fair value anchored on Black–Scholes, tested early in round 3, lost about 64,000 per strike.

The two write-ups that discuss a voucher delta hedge (19th, 583rd) both favour it. Without our cost inputs or the book's direction, whether our rejection was right for us stays open.

**On volatility.** [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) (28th) used one flat volatility of 0.20 in round 3 and added a parabolic correction across strikes in round 4. [JaneRT](https://github.com/heyman7913/imc-prosperity-4) list a flat volatility that missed the smile as their round-3 mistake.

**On the deep strikes.** Quoting VEV_6000 and VEV_6500 at a bid of 0 or 1 appears in several write-ups. In round 4, [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) noted one named counterparty (Mark 22) selling these strikes at 0. Our buy-at-zero rule matches this.

**On HYDROGEL.** DTU's fixed-peg market making on HYDROGEL kept buying into a 70-tick drawdown; in round 4 they added a three-state regime detector (pinned, trending, noisy). [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) (2nd, phase 2) instead traded HYDROGEL and VFE mean reversion around fixed values with symmetric thresholds, for +297,716 in this round.
