# Amazon — One-at-a-Time Sensitivity and Driver Rankings

## Purpose

This analysis evaluates how four adjustable assumptions affect Amazon's projected operating income, free cash flow to the firm (FCFF), and estimated equity value per share.

**Valuation date:** September 1, 2026  
**Model:** `analysis.py`  
**Calculation script:** `sensitivity_driver_ranking.py`  
**Results:** `Output/sensitivity_driver_ranking.csv`

## Method

Each driver was changed independently while the remaining assumptions were held at their base-case values.

Two symmetric ranges were tested:

- **Narrow:** ±0.5 percentage points
- **Wide:** ±1.0 percentage point

These ranges are illustrative comparisons, not statistically estimated confidence intervals or independently established plausible bounds.

## Base Valuation

The Python engine produced a base estimated equity value of **$104.81 per share**, using its exact WACC assumption of 10.53%.

The Streamlit dashboard previously displayed approximately $105.28 per share because its initial WACC slider used 10.5%.

This difference reflects input precision rather than a different investment conclusion. Both estimates remain preliminary.

## Valuation Sensitivity Results

| Driver | Narrow valuation swing | Wide valuation swing |
|---|---:|---:|
| WACC | $15.67 | $31.77 |
| Terminal growth | $12.55 | $25.44 |
| Operating margin adjustment | $11.76 | $23.52 |
| CapEx/revenue adjustment | $8.44 | $16.88 |

The values represent the absolute difference in estimated value per share between the low and high inputs for each driver.

### Valuation Driver Ranking

The ranking was identical under both tested ranges:

1. WACC
2. Terminal growth
3. Operating margin
4. Capital expenditures as a percentage of revenue

This indicates that discount-rate and terminal-growth assumptions have the largest effects on estimated share value within these tested ranges.

## Operating Profit Sensitivity

For the wide range:

| Driver | 2030 operating income swing |
|---|---:|
| Operating margin | $27,303.02 million |
| CapEx/revenue | $0 |
| WACC | $0 |
| Terminal growth | $0 |

Operating margin is the only adjustable driver in this test that directly changes operating income.

The zero impacts for other drivers reflect the model's current architecture, not a claim that capital spending and financing conditions cannot affect Amazon's profitability in practice.

## FCFF Sensitivity

For the wide range:

| Driver | 2030 FCFF swing |
|---|---:|
| Operating margin | $21,842.42 million |
| CapEx/revenue | $14,696.55 million |
| WACC | $0 |
| Terminal growth | $0 |

Operating margin has the largest tested effect on 2030 FCFF, followed by capital expenditures.

WACC and terminal growth do not change the underlying projected FCFF in the current model; they affect the present value of that cash flow.

## Range Robustness

The tested rankings remained unchanged when the symmetric input changes increased from ±0.5 to ±1.0 percentage point.

However, this does not establish robustness across all plausible uncertainty ranges. Different economic assumptions, segment-level growth shocks, depreciation responses, or wider nonlinear effects could change the rankings.

## Investment Interpretation

The sensitivity analysis reinforces the preliminary Watch / Defer recommendation.

Amazon's estimated equity value depends heavily on long-term valuation assumptions, particularly WACC and terminal growth, while operating margins and reinvestment determine projected cash flow generation.

The analysis does not resolve whether the model's base assumptions are sufficiently supported by market evidence.

## Limitations

- Only four dashboard-adjustable assumptions were ranked.
- Segment revenue-growth assumptions were not independently varied in this test.
- The ranges were selected for comparison, not established from historical volatility or expert forecasts.
- The model contains simplified accounting relationships.
- The sensitivity results do not independently validate the underlying forecasts, terminal value, or enterprise-to-equity bridge.

**Conclusion:** The one-at-a-time tests quantify the effects of the four adjustable assumptions. Rankings were stable across the two tested ranges, subject to the limitations above.