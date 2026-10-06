# Post-competition analysis tools

After the competition, Oscar directed a small offline lab to study two mechanisms that sit under every market-making strategy the team ran: **inventory-aware quoting** and **cancellation delay**. The lab was built later, with AI help, on **SYNTHETIC** data.

Read this page with three facts in mind:

- **Every number here is SYNTHETIC.** The price paths are hand-made rising and falling sequences, not Prosperity data.
- **None of the team's code, fills or logs went through the lab.** The team's code is not recovered on the machine where the lab was built. The lab says nothing about how our rounds actually went.
- **The lab's code:** [agentic-quant-research/platform/packages/imc-sim](https://github.com/oscar-chw/agentic-quant-research/tree/main/platform/packages/imc-sim).

Source for every number below: that package's `docs/QUOTE_STUDY_RESULTS.md` and `docs/QUOTE_POLICY.md`, and its README for the import example.

## Why these two mechanisms

The audit of the team's code (Codex, 2026), relayed, original files not published, shows inventory skew or inventory controls in several of our traders: the tutorial EMERALDS quotes, round-1 OSMIUM, the round-3 VFE fair value and the round-5 primary products. Skewing quotes by inventory trades profit for lower exposure. The lab asks how big that trade is, and what happens when old quotes cannot be pulled in time.

Whether Prosperity's own matching engine lets a quote outlive its tick is not established here, so the cancellation result is a general market-making lesson rather than a claim about the competition.

## Study 1: inventory-aware quotes give up opportunities

**Method.** Two policies quote around a centre with a fixed half-spread. The symmetric policy uses the fair price as the centre. The adjusted policy shifts the centre by inventory, following [Avellaneda and Stoikov's](https://math.nyu.edu/inmemoriam/avellaneda/HighFrequencyTrading.pdf) reservation price: r = s − q·γ·σ²·τ (price s, inventory q, risk aversion γ, volatility σ, time left τ). A long position lowers both quotes, which favours selling. Both policies see exactly the same synthetic sellers and buyers; their fills differ because their quotes differ. A fee of 0.1 per unit is charged, and leftover inventory is marked at the last price.

**SYNTHETIC results**, immediate cancellation, no queue ahead:

| Path | Symmetric P&L | Adjusted P&L | Peak inventory (sym / adj) | Inventory² × time (sym / adj) |
|---|---:|---:|---:|---:|
| Rising, 100 → 108 | 34.6 | −0.6 | 6 / 2 | 116 / 28 |
| Falling, 100 → 92 | −9.4 | −4.6 | 6 / 2 | 116 / 28 |

The adjusted policy carried far less inventory on both paths. That helped when the price fell and cost the whole directional gain when it rose. Lower exposure is not free.

With two units queued ahead of our orders the same pattern holds at smaller size: rising 23.2 against 1.7, falling −8.8 against −0.3.

## Study 2: cancellation delay changes the economics

**Method.** The same two policies, but a cancelled quote stays live for one more tick before the cancel is acknowledged.

**SYNTHETIC results**, one-tick cancellation delay:

| Path | Symmetric P&L | Adjusted P&L |
|---|---:|---:|
| Rising | 26.4 | −14.6 |
| Falling | −9.4 | −10.6 |

**What happened in the −14.6 case.** The adjusted policy bought two units at 99. At tick 4, an old ask at 99, already cancelled but not yet acknowledged, sold both units; a newer ask at 101 sold one more. Inventory went from +2 to −1. At tick 5 a remaining pending ask at 101 sold another unit, leaving −2. The price ended at 108, so the policy was short into a rising market.

Every order still respected the ±6 position bound, because the policy counted pending orders against its capacity. **Staying within limits did not make the execution good.** The fix would be another control choice, such as waiting for the cancel to be acknowledged before quoting again, and that would need its own frozen comparison. None was tuned into these results after seeing the loss.

## The accounting check

A small hand-worked case checks the accounting independently. Starting from cash 1,000, both policies buy one unit at 99. The adjusted policy sells it at 100 next tick; the symmetric policy's ask at 101 never fills. The final price is 98.

| Policy | Final cash | Inventory | Equity | P&L |
|---|---:|---:|---:|---:|
| Symmetric | 900.9 | 1 | 998.9 | −1.1 |
| Adjusted | 1,000.8 | 0 | 1,000.8 | 0.8 |

The lab also imports a saved log in a pinned community backtester format ([nabayansaha/imc-prosperity-4-backtester](https://github.com/nabayansaha/imc-prosperity-4-backtester)) and reports cash, fees, inventory breaches and fill markouts. Its two-instrument example ends at cash 901, equity 1,003 and P&L 3. The import path is ready for a real round log if one is recovered.

## What this does and does not show

- It shows, on hand-made paths, that inventory skew trades directional gain for lower exposure, and that stale quotes can flip a position against the trend while every limit holds.
- It does not show that the team's skew settings were wrong, or how much any round lost to either mechanism. That needs the team's logs: if one is recovered ([README](../README.md#limits)), the lab's importer can replace these SYNTHETIC cases with real fills.
