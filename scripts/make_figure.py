#!/usr/bin/env python3
"""Render assets/strategy-map.png: our approach against the top teams', per product type.

    python scripts/make_figure.py      (any Python with matplotlib)

Every row restates docs/top-teams-comparison.md or a round document, named in the last
field; no number appears that is not in those files. The verdict is that file's
"Would it have applied?" judgement, not a score: per-round scores are not recorded.
"""
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "strategy-map.png"

# Verdict -> marker colour. Validated as a categorical set (light surface, all pairs);
# every marker carries its text label, so colour is never the only cue.
VERDICTS = {
    "Same idea": "#2a78d6",
    "Partly or late": "#1baf7a",
    "Different": "#eb6834",
    "Field split": "#4a3aa7",
    "Not in our records": "#a3a29c",
}

# (round, product type, what we ran, what top teams did, verdict, source)
ROWS = [
    ("Tutorial", "Fixed-value product", "Fixed fair value 10,000,\ninventory-skewed quotes",
     "Same standard answer; some first\nmeasured the matching rules", "Same idea", "rounds/tutorial.md"),
    ("R1-R2", "Stable product (OSMIUM)", "Fixed fair value in R1,\nwall mid from R2",
     "Wall mid (midpoint of the\ndeep orders) from R1", "Partly or late", "top-teams-comparison.md"),
    ("R1", "Drift product (PEPPER_ROOT)", "Online slope estimate,\ndrift-aware buys, capped sells",
     "Buy to the limit early and hold;\nnever short", "Partly or late", "top-teams-comparison.md"),
    ("R1-R2", "Empty book side", "No rule recorded",
     "Quote very wide; a hidden\ntaker may hit it", "Not in our records", "top-teams-comparison.md"),
    ("R2", "Bot behaviour", "Seven research methods;\ndeployment unknown",
     "Recurring takers: same time,\nside and size across days", "Not in our records", "rounds/round-2.md"),
    ("R3", "Voucher delta hedge", "Hedge costed, then rejected:\ncost > gamma-scalp value",
     "Hedged (19th), delta-adjusted\nquotes (57th), others not", "Field split", "rounds/round-3.md"),
    ("R3", "Deep strikes (VEV_6000/6500)", "Buy at zero, hold to\nend of day",
     "Bid 0 or 1", "Same idea", "rounds/round-3.md"),
    ("R3-R4", "Trend vs. regime", "Kalman drift sign with a\nt-statistic gate (VFE only)",
     "Three-state regime detector;\nGaussian-mixture regimes", "Partly or late", "top-teams-comparison.md"),
    ("R4", "Named counterparties", "Traded signals from\nMarks 14, 38, 01 and 55",
     "Mostly not traded; Marks 14\nand 38 overfitted", "Different", "rounds/round-4.md"),
    ("R5", "Coverage of 50 products", "Market-made 9 of the 50",
     "Market-make all 50 as\na backbone", "Different", "rounds/round-5.md"),
    ("R5", "Cross-family value", "Gated one-lot residual\ntrade across 10 families",
     "Cross-family baskets collapsed\nout of sample", "Different", "rounds/round-5.md"),
    ("R5", "PEBBLES identity", "No rule recorded",
     "Five prices sum to about\n50,000; trade the gap", "Not in our records", "rounds/round-5.md"),
    ("R5", "Round-hundred jumps", "Two OXYGEN_SHAKE products\nmarket-made; no jump rule",
     "Fade jumps to a round\nhundred", "Not in our records", "rounds/round-5.md"),
    ("All", "Out-of-sample check", "Backtest on visible days 2-4;\ndecay written down",
     "Fit on two days, test on the\nthird; worst day must be positive", "Partly or late",
     "top-teams-comparison.md"),
]

INK, MUTED, RULE, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
COLS = [0.012, 0.075, 0.245, 0.495, 0.765]  # round, product, ours, top teams, verdict
ROW_H = 0.058


def main():
    fig = plt.figure(figsize=(16, 10.4), dpi=110, facecolor=SURFACE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(COLS[0], 0.965, "Our approach against the top teams', by product type",
            color=INK, fontsize=17, fontweight="bold", va="center")
    ax.text(COLS[0], 0.932, "IMC Prosperity 4, Team SHDC. Verdicts restate docs/top-teams-comparison.md and the "
            "round documents; ours from the relayed audit of the team's code. "
            "No scores: per-round scores are not recorded.", color=MUTED, fontsize=10.5, va="center")

    top = 0.885
    for x, head in zip(COLS, ["Round", "Product type", "What we ran", "What top teams did",
                              "Verdict  (source in docs/)"]):
        ax.text(x, top, head, color=MUTED, fontsize=10.5, fontweight="bold", va="center")
    ax.plot([COLS[0], 0.988], [top - 0.018] * 2, color=MUTED, lw=1)

    for i, (rnd, product, ours, theirs, verdict, src) in enumerate(ROWS):
        y = top - 0.05 - i * ROW_H
        ax.text(COLS[0], y, rnd, color=MUTED, fontsize=10.5, va="center")
        ax.text(COLS[1], y, product, color=INK, fontsize=10.5, fontweight="bold", va="center")
        ax.text(COLS[2], y, ours, color=INK, fontsize=10, va="center", linespacing=1.25)
        ax.text(COLS[3], y, theirs, color=INK, fontsize=10, va="center", linespacing=1.25)
        ax.scatter([COLS[4] + 0.006], [y + 0.007], s=110, marker="s", color=VERDICTS[verdict],
                   edgecolors=SURFACE, linewidths=2)
        ax.text(COLS[4] + 0.02, y + 0.007, verdict, color=INK, fontsize=10.5, va="center")
        ax.text(COLS[4] + 0.02, y - 0.013, src, color=MUTED, fontsize=8.5, va="center")
        ax.plot([COLS[0], 0.988], [y - ROW_H / 2] * 2, color=RULE, lw=0.8)

    fig.savefig(OUT, dpi=110, facecolor=SURFACE)
    print(OUT.relative_to(OUT.parent.parent))


if __name__ == "__main__":
    main()
