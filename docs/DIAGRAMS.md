# Diagrams

Every node is a strategy line, round or result in this write-up's documents; every label comes
from the README or `docs/rounds/*.md`. The team's code is not published, so "where" lines point
at the documents that record it. The README embeds diagrams 1 and 2; diagrams 3 and 4 are in
[top-teams-comparison.md](top-teams-comparison.md).

*If a diagram and the code disagree, the code wins.*

1. [Strategy map per round](#1-strategy-map-per-round)
2. [Round timeline](#2-round-timeline)
3. [Against the field: tutorial to round 3](#3-against-the-field-tutorial-to-round-3)
4. [Against the field: rounds 4 and 5](#4-against-the-field-rounds-4-and-5)

## 1. Strategy map per round

What each round's trader did, from fair value to the controls on its orders, one row per round, and who coded it by Oscar's account (labels from the [round documents](rounds/tutorial.md)):

```mermaid
flowchart TB
  subgraph RT["Tutorial, teammates: EMERALDS, TOMATOES"]
    direction LR
    T0F["EMERALDS fixed<br/>10,000; TOMATOES<br/>moving centre"]
    T0Q["market making"]
    T0R{{"EMERALDS quotes<br/>skewed by<br/>inventory"}}
    T0F -->|"fair value"| T0Q
    T0Q -->|"bid, ask"| T0R
  end
  subgraph RA["Round 1, teammates: OSMIUM, PEPPER_ROOT"]
    direction LR
    R1F["OSMIUM fixed<br/>value; PEPPER_ROOT<br/>online slope"]
    R1Q["OSMIUM takes,<br/>passive quotes;<br/>PEPPER_ROOT<br/>drift-aware buys"]
    R1R{{"inventory<br/>controls;<br/>capped sells"}}
    R1F -->|"value, slope"| R1Q
    R1Q -->|"takes, quotes"| R1R
  end
  subgraph RB["Round 2, teammates: same two, access bid"]
    direction LR
    R2F["ACO wall mid"]
    R2Q["ACO market<br/>making"]
    R2R{{"aims inventory-<br/>neutral"}}
    R2F -->|"value<br/>from book"| R2Q
    R2Q -->|"quotes"| R2R
  end
  subgraph RC["Round 3, teammates: HYDROGEL, VFE, 10 vouchers"]
    direction LR
    R3F["VFE filtered<br/>fair value"]
    R3Q["HYDROGEL MM<br/>+ take overlay;<br/>vouchers MM;<br/>deep strikes<br/>bought at zero"]
    R3R{{"VFE inventory<br/>skew; delta<br/>hedge rejected"}}
    R3F -->|"fair value"| R3Q
    R3Q -->|"quotes, takes"| R3R
  end
  subgraph RD["Round 4, Oscar: same, named counterparties"]
    direction LR
    R4F["HYDROGEL fixed<br/>anchor; VFE Kalman<br/>drift slope"]
    R4Q["HYDROGEL MM<br/>+ Mark signals;<br/>VFE counterparty<br/>target"]
    R4R{{"kept only if<br/>Kalman drift<br/>sign agrees,<br/>t-stat gate;<br/>stop-out, end-of-day"}}
    R4F ==>|"anchor; slope<br/>+ variance"| R4Q
    R4Q ==>|"signal<br/>targets"| R4R
  end
  subgraph RE["Round 5, Oscar: 50 products, 10 families"]
    direction LR
    R5F["Kalman or OU<br/>fair value; residual<br/>vs its family"]
    R5Q["MM on 9 of 50;<br/>cross-family<br/>residual trade"]
    R5R{{"warm-up, score,<br/>z-gap, spread<br/>gates; one lot"}}
    R5F ==>|"values,<br/>residuals"| R5Q
    R5Q ==>|"quotes;<br/>candidates"| R5R
  end
  RT -->|"next round"| RA
  RA -->|"next round"| RB
  RB -->|"next round"| RC
  RC -->|"next round"| RD
  RD ==>|"next round"| RE
  classDef data fill:#dbeafe,stroke:#1d4ed8,color:#0b1220
  classDef step fill:#f1f5f9,stroke:#475569,color:#0b1220
  classDef gate fill:#fef3c7,stroke:#b45309,color:#0b1220
  classDef out  fill:#dcfce7,stroke:#15803d,color:#0b1220
  classDef ext  fill:#f8fafc,stroke:#94a3b8,color:#0b1220,stroke-dasharray:4 3
  classDef key  fill:#ede9fe,stroke:#6d28d9,color:#0b1220,stroke-width:2px
  class T0F,T0Q,R1F,R1Q,R2F,R2Q,R3F,R3Q step
  class R4F,R4Q,R5F,R5Q key
  class T0R,R1R,R2R,R3R,R4R,R5R gate
```

Where in the code: the team's trader files are not published; every node is a strategy line in `docs/rounds/tutorial.md` to `docs/rounds/round-5.md`, and who coded which round is from [Who did what](../README.md#who-did-what). All diagrams: [docs/DIAGRAMS.md](DIAGRAMS.md).

## 2. Round timeline

Round by round, what changed between rounds and where the local replays warned:

```mermaid
flowchart TB
  T0["Tutorial, teammates<br/>fixed-value MM,<br/>inventory skew"]
  subgraph QUAL["Qualifier: rounds 1 and 2"]
    R1["Round 1, teammates<br/>fixed value; drift slope"]
    R2["Round 2, teammates<br/>wall mid; GP-UCB proposals"]
  end
  subgraph FIN["Finals: rounds 3 to 5, very likely the scored ones"]
    R3["Round 3, teammates<br/>vouchers MM; hedge rejected"]
    R4["Round 4, Oscar<br/>Kalman gate replaces<br/>5,000-tick gate"]
    R5["Round 5, Oscar<br/>Kalman/OU MM on 9 of 50;<br/>one-lot family gate"]
  end
  WARN{{"replay warnings,<br/>no go/no-go rule"}}
  RES["final: 904th of 18,803;<br/>algorithmic 917th"]
  T0 -->|"new: OSMIUM, PEPPER_ROOT"| R1
  R1 -->|"fixed value → wall mid"| R2
  R2 -->|"leaderboard reset; HYDROGEL,<br/>VFE, 10 vouchers added"| R3
  R3 ==>|"tape names<br/>counterparties"| R4
  R4 ==>|"50 products<br/>in 10 families"| R5
  R1 -.->|"LOCAL replay ≈63,464;<br/>notes: may overstate"| WARN
  R5 -.->|"LOCAL replay PnL decays,<br/>days 2–4; file not identified"| WARN
  FIN ==>|"very likely scored;<br/>no per-round scores"| RES
  classDef data fill:#dbeafe,stroke:#1d4ed8,color:#0b1220
  classDef step fill:#f1f5f9,stroke:#475569,color:#0b1220
  classDef gate fill:#fef3c7,stroke:#b45309,color:#0b1220
  classDef out  fill:#dcfce7,stroke:#15803d,color:#0b1220
  classDef ext  fill:#f8fafc,stroke:#94a3b8,color:#0b1220,stroke-dasharray:4 3
  classDef key  fill:#ede9fe,stroke:#6d28d9,color:#0b1220,stroke-width:2px
  class T0,R1,R2,R3 step
  class R4,R5 key
  class WARN gate
  class RES out
```

Where in the code: not published; sources are `docs/rounds/*.md`, [Results](../README.md#results) and [scoring](top-teams-comparison.md#how-the-rounds-were-scored) for the reset and the final ranks.

## 3. Against the field: tutorial to round 3

The field's idea against ours, rounds tutorial to 3 (teammates' rounds); each edge says how our version differs:

```mermaid
flowchart LR
  subgraph FA["Field: public P4 write-ups, placements as stated"]
    F1["tested the matching<br/>rules in the tutorial (93rd)"]
    F2["wall mid fair value<br/>(4th; P3 2nd)"]
    F3["quote wide into an<br/>empty book side (4th)"]
    F4["drift product: buy to<br/>the limit early, hold (4th)"]
    F5["recurring bot takers, from<br/>raw trades day vs day (4th)"]
    F6["voucher delta hedge (19th);<br/>583rd call not applying<br/>theirs a mistake"]
    F7["fitted a volatility smile<br/>after flat vol failed (28th)"]
  end
  subgraph OA["SHDC, from the records"]
    O1["no record of<br/>measuring them"]
    O2["fixed value in round 1,<br/>wall mid from round 2"]
    O3["no such rule recorded"]
    O4["online slope, drift-aware<br/>buys, capped sells"]
    O5["research methods,<br/>none known to ship"]
    O6["hedge costed,<br/>then rejected"]
    O7["vouchers market-made;<br/>vol model not recorded"]
  end
  F1 -->|"not in our records"| O1
  F2 -->|"same idea,<br/>one round later"| O2
  F3 -->|"would have applied,<br/>rounds 1 and 2"| O3
  F4 -->|"partly: holding the<br/>limit not recorded"| O4
  F5 -->|"would have applied,<br/>round 2 only"| O5
  F6 ==>|"differs; open: inputs,<br/>book direction unrecorded"| O6
  F7 -->|"unknown"| O7
  classDef data fill:#dbeafe,stroke:#1d4ed8,color:#0b1220
  classDef step fill:#f1f5f9,stroke:#475569,color:#0b1220
  classDef gate fill:#fef3c7,stroke:#b45309,color:#0b1220
  classDef out  fill:#dcfce7,stroke:#15803d,color:#0b1220
  classDef ext  fill:#f8fafc,stroke:#94a3b8,color:#0b1220,stroke-dasharray:4 3
  classDef key  fill:#ede9fe,stroke:#6d28d9,color:#0b1220,stroke-width:2px
  class F1,F2,F3,F4,F5,F6,F7 ext
  class O1,O2,O3,O4,O5,O7 step
  class O6 key
```

Where in the code: not published; each node is a row of [top-teams-comparison.md](top-teams-comparison.md) or a line of `docs/rounds/*.md`.

## 4. Against the field: rounds 4 and 5

Rounds 4 and 5 (Oscar's rounds), the same way:

```mermaid
flowchart LR
  subgraph FB["Field: public P4 write-ups, placements as stated"]
    F8["regime detector after<br/>a fixed peg broke (28th)"]
    F9["named counterparties mostly<br/>not traded; Marks 14, 38<br/>failed a held-out day (57th)"]
    F10["market-make all 50,<br/>then add ideas (4th)"]
    F11["PEBBLES prices sum<br/>to about 50,000"]
    F12["round-hundred jumps revert,<br/>OXYGEN_SHAKE above all"]
    F13["fit two days, test the third;<br/>worst day must be positive"]
    F14["cross-family baskets<br/>collapsed out of sample (4th)"]
  end
  subgraph OB["SHDC, from the records"]
    O8["Kalman drift sign,<br/>t-stat gate, VFE only"]
    O9["traded Marks<br/>14, 38, 01 and 55"]
    O10["market making on<br/>9 of 50 products"]
    O11["no PEBBLES rule recorded"]
    O12["two OXYGEN_SHAKE products<br/>market-made"]
    O13["backtest on days 2–4;<br/>PnL decayed, no rule acted"]
    O14["one-lot cross-family<br/>residual gate"]
  end
  F8 -->|"a version of it,<br/>for one product"| O8
  F9 -->|"their held-out test is<br/>the one we needed"| O9
  F10 -->|"would have applied"| O10
  F11 -->|"would have applied"| O11
  F12 -->|"partly: which two<br/>not recorded"| O12
  F13 ==>|"would have measured<br/>the decay directly"| O13
  F14 -->|"same class of idea;<br/>gates and one lot bound it"| O14
  classDef data fill:#dbeafe,stroke:#1d4ed8,color:#0b1220
  classDef step fill:#f1f5f9,stroke:#475569,color:#0b1220
  classDef gate fill:#fef3c7,stroke:#b45309,color:#0b1220
  classDef out  fill:#dcfce7,stroke:#15803d,color:#0b1220
  classDef ext  fill:#f8fafc,stroke:#94a3b8,color:#0b1220,stroke-dasharray:4 3
  classDef key  fill:#ede9fe,stroke:#6d28d9,color:#0b1220,stroke-width:2px
  class F8,F9,F10,F11,F12,F13,F14 ext
  class O8,O9,O10,O11,O12,O14 step
  class O13 key
```

Where in the code: not published; each node is a row of [top-teams-comparison.md](top-teams-comparison.md) or a line of `docs/rounds/*.md`. The field side draws on the nine Prosperity 4 write-ups listed in [credits](credits.md) (plus Prosperity 3 for wall mid); placements are as each source states them.
