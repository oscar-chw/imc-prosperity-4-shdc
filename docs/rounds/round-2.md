# Round 2

Sources: audit of the team's code (Codex, 2026), relayed; original files not published (`ROUND_2/analysis/run_analysis.py:405-519` for GP-UCB). Product facts are as other teams' write-ups state them; see [credits](../credits.md). The manual challenge is in [manual-rounds.md](../manual-rounds.md#round-2-invest-and-expand).

## Products

The same two products as round 1, ASH_COATED_OSMIUM (ACO) and INTARIAN_PEPPER_ROOT, plus a mechanism for bidding for extra market access. The write-ups disagree on its rules: one says the best bid was 0, another cites a bid of 151 units. We have not confirmed them.

## Our hypothesis

The records hold the strategy, not the reasoning. Switching ACO from a fixed value to wall-mid implies the team no longer trusted a hard-coded fair value and wanted one read from the book.

## Strategy

From the audit:

- **ACO:** wall-mid fair value; market making that aims to stay inventory-neutral.
- **PEPPER_ROOT:** the audit does not record the round-2 logic.
- **Research only, deployment unknown:** DenStream clustering, recursive least squares, micro-price, a hidden Markov model, Hawkes processes, Kyle's lambda and Kelly sizing were explored in analysis scripts. The audit cannot say whether any reached the submitted trader.
- **GP-UCB parameter proposals.** A Gaussian-process model with a constant × Matérn(2.5) + white-noise kernel was fitted to past backtest results over two parameters, `PASSIVE_CAP` and `CLEAR_OFFSET`. It proposed the next pair to try by maximising the upper confidence bound μ + 2σ: the predicted result plus two standard deviations, which favours pairs that are either good or still uncertain. It ran on 3 observations and produced one proposal. It was a proposal tool, not a closed optimisation loop.

## Result

- Official: no per-round score is recorded.

  TODO-OSCAR: Q1 — round-2 algorithmic score and rank, and what the team bid for market access.
- No local backtest figure is recorded for this round.

## Mistakes

The records show none for this round.

TODO-OSCAR: Q4 — what went wrong in round 2, and when did the team notice?

## What top teams did

- **Recurring takers.** Between rounds 2 and 3, [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) found bot orders that came back at the same timestamp, side and size on consecutive days. They estimate it would have been worth 70k to 100k in round 2. The pattern did not persist into later rounds.
- **A drift line with asymmetric quotes.** [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) (57th, as stated) modelled PEPPER_ROOT as a starting price plus drift × time and quoted asymmetrically around that line.
- **Scale of the round.** [Ape108](https://github.com/Ape108/IMC-Prosperity-4) (42nd, as stated) report 475k for this round alone.

The comparison: our wall-mid switch matches the top teams' fair value for ACO. Our research list is wide (seven methods), but nothing recorded shows which reached a submission. The top teams' gains here came from one narrow fact about the bots, found by looking at the raw trades day against day.
