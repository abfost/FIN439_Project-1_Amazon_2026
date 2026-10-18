# Amazon Independent Validation

## Purpose

Document selected independent calculations, changed-input testing, accounting reconciliation, and limitations of the preliminary Amazon valuation model.

**Company:** Amazon.com, Inc. (AMZN)  
**Valuation date:** September 1, 2026  
**Units:** USD millions unless otherwise indicated.

## Test A: Known-Answer FCFF Calculation

The following is a synthetic arithmetic check, not a reconciliation of Amazon's complete valuation engine to an external training-case solution.

Inputs:

- EBIT: $1,000 million
- Tax rate: 20%
- Depreciation: $100 million
- Capital expenditures: $250 million
- Change in operating NWC: $50 million

Independent calculation:

After-tax operating income = $1,000 × (1 − 0.20) = $800 million.

FCFF = $800 + $100 − $250 − $50 = **$600 million**.

**Expected result:** $600 million  
**Observed result:** $600 million  
**Difference:** $0 million  
**Status:** PASS

Test file: `test_known_answer.py`

This verifies the standalone FCFF arithmetic using synthetic inputs. It does not establish that the complete Amazon forecast or valuation engine has been independently reconciled.

## Test B: Changed-Input Test

A directional sensitivity test was performed using a one-percentage-point increase in the 2026 capital-expenditure-to-revenue assumption.

**Original adjustment:** 0.00 percentage points  
**Changed adjustment:** +1.00 percentage point  
**2026 forecast revenue:** $840,334 million

Independent expectation:

Additional capital expenditures = $840,334 × 0.01 = **$8,403.34 million**.

Expected 2026 capital expenditures = $168,066.80 + $8,403.34 = **$176,470.14 million**.

Expected immediate directional effects:

- Capital expenditures increase by $8,403.34 million.
- Ending cash decreases by $8,403.34 million, all else equal.
- Ending property, plant, and equipment increases by $8,403.34 million, all else equal.
- Estimated equity value per share decreases.

Observed results recorded during testing:

- 2026 capital expenditures: $176,470.14 million
- Ending cash: $71,894.53 million
- Ending PP&E: $462,090.14 million
- Estimated value per share: approximately $96.80

**Status:** PASS for the selected directional and arithmetic expectations.

Evidence: `Output/ai_off_changed_input_test.png`

The full precommit evidence and any AI-off qualification should be assessed using the original timestamped record; this summary is not itself proof of an independently precommitted test.

## Test C: Historical Accounting Reconciliation

Amazon's reported fiscal-year 2025 balance sheet provides:

- Total assets: $818,042 million
- Total liabilities: $406,977 million
- Total shareholders' equity: $411,065 million

Independent calculation:

$818,042 − $406,977 − $411,065 = **$0 million**.

**Status:** PASS

This verifies the historical balance-sheet identity for these reported totals, not every forecast account.

## Additional Engine Verification

Five automated valuation arithmetic tests passed using `test_valuation_engine.py`.

Preliminary financial-statement linkage checks passed using `test_three_statements.py`.

A deliberately invalid combination of WACC = 8% and terminal growth = 8% caused the valuation engine to raise:

`ValueError: Invalid terminal growth rate`

Evidence: `Output/invalid_growth_engine_test.png`

The project dependencies installed successfully in a separate Python environment, the five valuation tests passed, and the Streamlit dashboard launched successfully.

This was not a completely isolated GitHub-clone cold run.

## Model Limitations

The model remains preliminary. Material areas requiring further verification include:

- The treatment of the partial 2026 forecast period
- Capital expenditure and depreciation assumptions
- Stock-based compensation
- Net working capital assumptions
- Basic versus diluted share counts
- Cash, debt, and lease treatment in the enterprise-to-equity bridge
- Terminal-value dependence
- Comparable-company accounting and multiple consistency
- Full independent reconciliation of forecast financial statements

**Overall conclusion:** Selected arithmetic and directional checks passed, but the complete valuation is not fully independently validated. The investment recommendation remains Watch / Defer.
## Enterprise-to-Equity Bridge Verification

The current analysis.py engine produced the following base-case results (USD millions except per-share amounts):

- Enterprise value: $1,136,022.09
- Less long-term debt carrying value: $128,894.00
- Add cash and equivalents: $78,213.00
- Add marketable securities: $44,775.00
- Calculated equity value: $1,130,116.09
- Shares outstanding: 10,783 million
- Estimated equity value per share: $104.81

Independent arithmetic:
$1,136,022.09 - $128,894.00 + $78,213.00 + $44,775.00 = $1,130,116.09 million.

$1,130,116.09 / 10,783 = approximately $104.81 per share.

Result: PASS — Arithmetic reconciliation.

Limitation: This confirms mathematical consistency of the selected bridge inputs. It does not independently establish that all debt-like claims, lease liabilities, nonoperating assets, or dilution adjustments have been appropriately included.
## Comparable-Company Definition Check

The peer valuation calculation uses market capitalization = share price × shares outstanding, enterprise value = market capitalization + debt − cash/investments, EV/Revenue = enterprise value ÷ trailing revenue, and P/E = market capitalization ÷ trailing net income.

Walmart, Microsoft, and Alphabet were chosen as business-line reference points for Amazon's retail, cloud, and advertising activities rather than as identical business models.

The arithmetic definitions are consistent within peer_valuation.py. However, the underlying source values have not been fully standardized. In particular, cash and short-term investments, debt carrying values versus contractual obligations, trailing earnings periods, and historical share prices require reconciliation.

Because these definitions are unresolved, the peer multiples are preliminary screening evidence. They are not used to calculate a definitive peer-implied Amazon share price, and they do not independently validate the DCF.

Status: PARTIAL — Formula definitions reviewed; full input-definition consistency not established.
## Published FIN 43900 Training-Case Reconciliation

Source: FIN 43900 Week 3 Student Handout
https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/student-handout.md

A standalone DCF calculator was tested against the professor's published training-case answers.

Results (USD millions except per-share amounts):

- Year 1 FCFF: $108.00 — PASS
- Year 1 discounted FCFF: $98.18 — PASS
- Terminal value: $1,894.65 — PASS
- Enterprise value: $1,624.87 — PASS
- Equity value per share: $27.50 — PASS
- Increasing WACC from 10% to 11% reduced enterprise value — PASS

All published numerical checks reconciled within rounding tolerance.

Evidence:
- test_training_case.py
- Output/training_case_validation.png

Limitation: This validates the standalone training-case DCF calculation, not the complete connected Amazon forecasting engine.