# Amazon Three-Statement Model Validation

## Current Development Status

The preliminary model calculates financial projections for 2026–2030.

Completed components:
- Segment revenue forecasts
- Operating income forecasts
- Preliminary net income forecasts
- Operating working capital forecast
- Capital expenditure forecast
- Depreciation and net PP&E roll-forward
- Preliminary operating cash flow and cash balance roll-forward
- Preliminary FCFF calculations

## Aggregate Balance Sheet Diagnostic

The model reports an aggregate balance sheet difference of approximately zero for each forecast year from 2026 through 2030.

This result demonstrates internal consistency under the current simplified assumptions. It does not independently verify that all forecast assets, liabilities, and equity accounts are complete or correctly estimated.

## Remaining Limitations

1. Debt issuance, repayments, and interest expense are not yet explicitly forecast.
2. Lease assets, lease liabilities, and lease cash flows need separate treatment.
3. Marketable securities and other noncurrent accounts are currently held constant.
4. Stock-based compensation, deferred taxes, and other noncash items require consistent treatment.
5. Forecast depreciation relies on a preliminary assumption.
6. Operating working capital uses aggregate accounts that include items labeled "and other."
7. Financing and investing cash flows beyond modeled CapEx have not been fully developed.
8. Independent validation and changed-input tests remain necessary.

## Valuation Implications

Preliminary FCFF results should not be described as final fair-value estimates.

Before the final investment recommendation, the model requires:
- Documented valuation assumptions and sensitivity ranges
- WACC and terminal value calculations
- Enterprise-value-to-equity-value reconciliation
- An appropriate valuation-date share count
- Independent checks and scenario analysis

Status: Preliminary model working; full validation incomplete.