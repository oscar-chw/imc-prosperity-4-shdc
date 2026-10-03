# Prosperity 3: learning reference only

**Nothing on this page is part of our Prosperity 4 result.** Prosperity 3 is the previous edition. Oscar says he learned from its public write-ups, and mentions a second-placed team's repository without naming it. The summaries below are in our words; placements are as each source states them.

## The write-ups

| Write-up | Placement (as stated) | What it records |
|---|---|---|
| [Frankfurt Hedgehogs](https://github.com/TimoDiehm/imc-prosperity-3) | 2nd of 12,000+ | Price stable products from the "wall mid", the midpoint of the deep orders. A named trader who bought daily lows and sold highs could be followed. They traded basket-premium reversion with a half hedge. Fit the volatility smile with a parabola. Prefer a stable region of parameters to the single best backtest. Explain a strategy from first principles or treat its backtest as noise. |
| [CMU Physics](https://github.com/chrispyroberts/imc-prosperity-3) | 7th, 1st USA | A volatility-curve model broke on submission day and dropped them to 241st before they recovered. Static parameters were fragile. Conversion arbitrage with negative tariffs brought them back to 8th. |
| [Alpha Animals](https://github.com/CarterT27/imc-prosperity-3) | 9th, 2nd USA | An honest bug list: a position-limit bug switched off basket trading for a whole round, and their backtester could not model conversions. |
| [Ding Crab](https://github.com/angus4718/imc-prosperity-3-public) | 28th algorithmic | A short, candid account of one missed arbitrage. |

Earlier editions, for tooling:

- [jmerle's Prosperity 2 repository](https://github.com/jmerle/imc-prosperity-2) (9th, as stated) is the origin of the open backtester and visualiser that most teams fork; the visualiser our team used descends from jmerle's work ([credits](credits.md)).
- [Linear Utility](https://github.com/ericcccsliu/imc-prosperity-2) (Prosperity 2, 2nd) built their own backtester with parameter grids and a dashboard that lines up every product on one clock.

## How it carried into Prosperity 4

- **Wall mid** carried over directly: our round-2 trader used it, and so did the 4th-placed team ([round 2](rounds/round-2.md)).
- **The volatility smile did not.** In Prosperity 3 a fitted smile paid; in Prosperity 4 the 4th-placed team found implied volatility stable per strike, while others still fitted one ([round 3](rounds/round-3.md)).
- **Following named traders mostly did not.** Prosperity 3's insider-style trader was strongly tradeable; Prosperity 4's named counterparties were mostly too weak ([round 4](rounds/round-4.md)).
