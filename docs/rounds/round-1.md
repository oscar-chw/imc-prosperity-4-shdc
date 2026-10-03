# Round 1

Sources: audit of the team's code (Codex, 2026), relayed; original files not published (`ROUND_1/trader.py`). Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-1-auction).

## Products

- **ASH_COATED_OSMIUM** (position limit 80): a price that stays near 10,000 with a spread of about 16.
- **INTARIAN_PEPPER_ROOT** (limit 80): a price with a steady upward drift, about +1,000 per day.

Both descriptions are stated by two or more top-team write-ups (for example [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) and [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4)).

## Our hypothesis

The records hold the strategy, not the reasoning. The strategy implies: OSMIUM has a fixed fair value, so mispriced orders can be taken and the rest of the book quoted; PEPPER_ROOT drifts, so the drift slope is worth estimating and buying ahead of it pays.

## Strategy

From the audit:

- **OSMIUM:** take any order mispriced against a fixed fair value, then quote passively, with inventory controls. The ask is widened depending on the order-book imbalance; the audit does not give the rule's direction or size.
- **PEPPER_ROOT:** estimate the drift slope online, tick by tick; buy with the drift in mind; cap the size of sells.

## Result

- Official: no per-round score is recorded.

  TODO-OSCAR: Q1 — round-1 algorithmic score and rank, if the Prosperity portal still shows them.
- **LOCAL BACKTEST, NOT OFFICIAL:** about 63,464 as a 3-day mean (audit).

## Mistakes

What the records show: the team's own FINDINGS.md warns that the 10k-tick local replay may overstate this result. How far it overstated is not recorded.

TODO-OSCAR: Q4 — what went wrong in round 1, and when did the team notice?

## What top teams did

- **A better fair value.** [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (4th, as stated) priced OSMIUM from the "wall mid": the midpoint of the deep, large orders rather than the best bid and ask, which moves with small noisy orders. The idea comes from [Frankfurt Hedgehogs](https://github.com/TimoDiehm/imc-prosperity-3) in Prosperity 3. Our round-1 trader used a fixed value; our round-2 trader switched to wall-mid ([round 2](round-2.md)).
- **Quoting into an empty side.** The same team noticed that when one side of the book is empty, a hidden taker may still hit a quote placed far away, so they quoted very wide there. [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) lists missing this as a lesson. Our records show no such rule.
- **Inventory skew is not always worth it.** [DTU Quant Lab](https://github.com/DataAthleteChamp/dtu-quant-lab-imc-prosperity-4) (28th, as stated) measured that an Avellaneda–Stoikov style inventory skew cost them about 16.6k in backtest and used a fixed anchor instead.
- **PEPPER_ROOT: reach the limit and hold.** Most top teams bought to the position limit early and never shorted. Une Baguette Fromage solved the timing as a dynamic program over time and inventory; Alpha Search accumulated, traded the reversion, then unwound late. Our trader estimated the slope and capped sells. Whether it held the full limit is not recorded.
