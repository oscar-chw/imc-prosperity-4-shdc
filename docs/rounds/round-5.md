# Round 5

Sources: audit of the team's code (Codex, 2026), relayed; original files not published. Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-5-news-portfolio).

**Who:** Oscar coded this round ([who did what](../../README.md#who-did-what)).

## Products

Fifty new products in ten families of five: GALAXY_SOUNDS, SLEEP_POD, MICROCHIP, PEBBLES, ROBOT, UV_VISOR, TRANSLATOR, PANEL, OXYGEN_SHAKE and SNACKPACK. [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) report a position limit of 10 units per product.

## Our hypothesis

The records hold the strategy and a decision document. The strategy implies: a handful of products behave like single mean-reverting series that can be market-made with a filtered fair value; and products in the same family share a common component, so a product far from its family is likely to move back.

## Strategy

From the audit:

- **Nine primary products** (five SLEEP_POD, two OXYGEN_SHAKE, two GALAXY_SOUNDS): per-product market making with a fair value from a Kalman filter or an Ornstein–Uhlenbeck (mean-reverting) model, and quotes adjusted for inventory.
- **A cross-family gate across all 50 products.** For each family, an online estimate of each product's residual against its family. A trade fires only when it passes every gate: a warm-up period, a score threshold, a minimum gap in z-score, and a spread check. Size is one lot.
- **Two execution variants** were backtested for the cross-gate portfolio: passive (quote and wait) and take-only (cross the spread).

## Result

- Official: per-round scores were not recorded; only the final result is.
- **LOCAL BACKTEST, NOT OFFICIAL**, the round-5 cross-gate portfolio replay (local) on the visible days 2–4: 127,494 passive and 165,281 take-only. The audit does not say whether these are totals or per-day values.

## Mistakes

What the records show:

- **The backtest PnL decays across the visible days**, and the team's decision document states a risk that the hidden test days behave differently.
- **The submitted file is not identified.** The decision document names `submissions/r5_portfolio_cross_gate_v01.py`, which differs from the root `ROUND_5/trader.py`. The records cannot say which one ran.

The README derives the costliest mistake of the competition from these records ([What I learned](../../README.md#what-i-learned)).

## What top teams did

- **Broad market making as the backbone.** Several top teams quoted every product and added a few targeted ideas on top ([Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4); [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4)). We market-made nine of the fifty.
- **An exact identity in PEBBLES.** The five PEBBLES prices summed to about 50,000, apart from some steps, so any gap was tradeable. Stated by several teams, including [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) and [JaneRT](https://github.com/heyman7913/imc-prosperity-4). Our records show no PEBBLES rule.
- **Jumps to round hundreds that revert.** Some prices, OXYGEN_SHAKE_CHOCOLATE above all, jumped to a round-hundred level and then reverted. rat_hunters measured that after a ±100 move the next move reversed it 85% of the time; for DTU, plain inside-spread market making on a dislocated OXYGEN_SHAKE_CHOCOLATE book earned +587,831, 84% of their round-5 algorithmic total. [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) missed it and wrote about why. We traded two OXYGEN_SHAKE products; which two is not recorded.
- **Pairs inside SNACKPACK.** VANILLA minus RASPBERRY was the cleanest spread for rat_hunters.
- **Cross-family searches failed out of sample.** Une Baguette Fromage found that baskets mined across families looked strong in sample and collapsed out of sample; rat_hunters showed that random walks produce many "cointegrated" pairs by chance; Alpha Search note that accepting a basket when any one of three folds passes p < 0.05 gives a false-positive rate of about 14%. Our cross-family residual gate is in this class of idea. Its gates and one-lot size limit the damage. The records do not separate the gate's PnL from the rest of the portfolio, so the decaying portfolio backtest cannot be attributed to it.
- **A worst-day rule.** DTU shipped a strategy only if its worst single backtest day was positive, which removed about 80% of their ideas.
- **Closest to our rank.** [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) (583rd) report a round-5 strategy that scored +144,786 on the portal backtest and −56,117 live, because EMA seeds hard-coded from the sample data no longer fit the live data.

For scale: DTU gained +702,835 in this round alone, and rat_hunters +701,157.
