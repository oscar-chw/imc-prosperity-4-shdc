# Pair trading: what the textbook says (post-competition notes)

Post-competition study notes, written with AI assistance from standard references. They are not Oscar's words and not what the team did; they are the background his lesson in the [README](../README.md#what-i-learned) points to.

1. **Test the spread, not the correlation.** Two prices can be highly correlated while their spread drifts away for good. The test is whether the spread is stationary: the Engle–Granger two-step (regress one price on the other, then an ADF test on the residuals, with Engle–Granger rather than standard ADF critical values), or Johansen's test for three or more series.
2. **Estimate the hedge ratio.** OLS of one price on the other gives β, but the answer depends on which is the dependent variable; total least squares treats both alike; a Kalman filter gives a time-varying β when the relationship drifts.
3. **Measure the speed of reversion.** Fit an AR(1), s(t) = c + φ·s(t−1) + ε, to the spread; the OU rate is κ = −ln φ per step and the half-life is ln 2 / κ. A half-life longer than the trading horizon rules the pair out.
4. **Trade the z-score, with stops.** Enter when the spread's z-score, over a lookback of a few half-lives, passes a threshold; exit near zero; stop out when the z-score keeps widening, a trade outlives several half-lives, or a rolling cointegration test fails (a structural break).
5. **Validate out of sample, net of costs.** Select pairs and fit parameters on one period, trade on another, and count every pair screened: among many random series some will look cointegrated by chance.

References: R. F. Engle and C. W. J. Granger, "Co-integration and error correction: representation, estimation, and testing", *Econometrica* 55(2), 1987; G. Vidyamurthy, *Pairs Trading: Quantitative Methods and Analysis*, Wiley, 2004.
