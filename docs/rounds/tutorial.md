# Tutorial round

Sources: audit of the team's code (Codex, 2026), relayed; original files not published. Other teams' work is linked where it is used; full list in [credits](../credits.md).

## Products

Two practice products:

- **EMERALDS**, which other teams' tooling models as a product with a fixed fair value of 10,000 ([chrispyroberts' Prosperity 4 backtester](https://github.com/chrispyroberts/imc-prosperity-4)).
- **TOMATOES**, a product whose price wanders without a fixed anchor (same source).

## Our hypothesis

The records hold the strategy, not the reasoning behind it. The strategy implies two beliefs: EMERALDS has a known fair value of 10,000, and TOMATOES reverts towards a moving centre, so quoting around that centre earns the spread.

## Strategy

From the audit:

- **EMERALDS:** fixed fair value 10,000; market making with quotes skewed by inventory, so a long position moves both quotes down to encourage selling and a short position moves them up.
- **TOMATOES:** mean-reverting market making.

## Result

No tutorial score is recorded, and no local backtest figure either.

## Mistakes

The records show none for this round.

TODO-OSCAR: Q4 — did anything in the tutorial go wrong or carry a wrong belief into round 1?

## What top teams did

- [Dark Forest Hunter](https://github.com/Leo-Hawking/IMC-Prosperity-4-Review) (93rd, as stated) used the tutorial to pin down the matching rules: no queue for resting orders, and the best price fills first. That is the kind of fact that decides whether passive quotes ever fill, and it is cheap to test before the scored rounds.
- [chrispyroberts](https://github.com/chrispyroberts/imc-prosperity-4) built a Monte Carlo backtester for the tutorial products with a dashboard, so strategies could be scored on many simulated days rather than the few days of sample data.

The comparison: our tutorial strategy matches the standard answer for a fixed-value product. Nothing recorded shows that the team measured the matching rules or simulated beyond the sample days.
