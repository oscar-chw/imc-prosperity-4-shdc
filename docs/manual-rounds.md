# Manual rounds

Our manual total is 147,209, 1,132nd of 18,803 (top 6.02%). Source: [leaderboard screenshot](../assets/leaderboard/manual-global-1132.jpg), taken 2026-06-01.

That is more points than our algorithmic total (86,750) but a worse rank (algorithmic was 917th). Points are only comparable within a track, so the manual result is the weaker of the two against the field.

**What the records hold about our manual submissions: nothing.** The audit covers trader code only, and no record holds our answers, our reasoning or a per-round manual score. Each section below therefore describes the problem and what top teams did; our submissions are not recorded.

Problem descriptions are as top-team write-ups state them; see [credits](credits.md).

## Round 1: auction

Two goods, DRYLAND_FLAX (bought back at 30) and EMBER_MUSHROOM (bought back at 20, with a fee of 0.10), sold in a call auction: one clearing price, orders filled by price then time. The submission is a price and quantity for each.

What top teams did: [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) (1st on this manual round, as stated) wrote an exact simulator of the auction and brute-forced every price and quantity, for 87,995. The observation several write-ups share: sit one unit below the point where the clearing price jumps.

## Round 2: invest and expand

A budget of 50,000 split across three pillars: Research (logarithmic return), Scale (linear return) and Speed (a multiplier that depends on your rank against other teams). The Speed pillar makes it a game against the crowd, not a single-player optimisation.

What top teams did: [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) and [JaneRT](https://github.com/heyman7913/imc-prosperity-4) both reached about 15/43/42 after modelling what the crowd would choose; Une Baguette Fromage queried language models repeatedly, under several player archetypes, to stand in for the crowd, and report 217,869. [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) put nothing on Speed and scored 24,233, which they list as a mistake.

## Round 3: two-bid game

Submit two bids for goods whose reserve prices are uniform from 670 to 920 in steps of 5, resold at 920. The second bid is penalised (cubically) if it is below the average second bid of the field, so it again depends on the crowd.

What top teams did: the Nash solution is near 751/836. Teams then shifted the second bid up as insurance against a high field: [Alpha Search](https://github.com/fabianbaiertum/IMC-Prosperity-4) chose 751/841 at a stated cost of about 0.14% of modelled PnL; [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) ran nine crowd scenarios and chose 766/861. The field's average second bid turned out to be 859 (as both Team Ryan Challman and Une Baguette Fromage report). [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) bid 756/852 for 74,710.

## Round 4: exotic options

A portfolio of options on AETHER_CRYSTAL (spot 50, very high volatility): vanillas at two expiries, a chooser, a binary put and a knock-out put. Scored on 100 simulated price paths, so luck mattered a lot.

What top teams did: [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) traded expected value against tail risk (CVaR), hedged heavily and realised 36,929, which they call over-hedging. [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) used a mean–variance portfolio for +65,024. [JaneRT](https://github.com/heyman7913/imc-prosperity-4) priced the knock-out with a discrete barrier rather than a continuous one. [Team Infinite 88](https://github.com/Chamoy-code/imc-prosperity-4-challenge) scored +2,826.

## Round 5: news portfolio

A budget of 1,000,000 to spread, long or short, over nine goods, guided by headlines shown as an image, with a fee that grows with the square of position size.

What top teams did: the consensus calls were short Lava Cake (strongest), long Thermalite Core, long Sulfur Reactor and short Pyroflex Cells. Because the fee is quadratic, the optimal size is well below "all in": [Team Ryan Challman](https://github.com/nathanw3456/Prosperity_4_Writeup) stopped at 65% of the budget and [Une Baguette Fromage](https://github.com/Durpie-Git/imc-prosperity-4) at 78%. Reported results: Team Ryan Challman +98,201, Une Baguette Fromage 99,373, [rat_hunters](https://github.com/rmtf1111/imc-prosperity-4) +104,014.
