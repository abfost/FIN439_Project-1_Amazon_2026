Amazon.com, Inc. — Project 1
VALIDATION AND AI USE RECORD
Course:  FIN 43900
Company:  Amazon.com, Inc. (AMZN)
Valuation date:  September 1, 2026
Record status:  Completed documented tests; remaining model limitations explicitly disclosed
1. AI Use Disclosure
ChatGPT was used extensively to assist with Python implementation, debugging, financial-model structure, documentation drafting, and explanations of valuation concepts. The author remained responsible for reviewing and accepting the calculations, assumptions, code changes, and written conclusions.
AI-generated suggestions were not treated as independently verified financial evidence. Historical data, accounting treatments, assumptions, valuation inputs, and model outputs require review against dated source filings and applicable project requirements. AI assistance also informed the preparation and wording of this validation record and the setup of the standalone known-answer check.
2. Technical Checks Performed
•	Historical 2025 balance-sheet reconciliation checks.
•	Preliminary 2026–2030 income statement, cash flow, PP&E, and working-capital linkage checks.
•	Five valuation arithmetic checks covering operating margins, capital expenditures, discounting, terminal value, and the enterprise-value-to-equity bridge.
•	Interactive dashboard checks showing that operating-margin and CapEx assumption changes affect forecast financial statements and estimated valuation.
•	Reset-to-base-case control and dashboard functionality.
These checks passed in the development tests performed under the model’s existing simplifying assumptions. A passing arithmetic or reconciliation check should not be interpreted as independent verification of the underlying accounting choices or forecasts.
3. Known-Answer Validation — Standalone FCFF Formula
Objective: Verify the arithmetic implementation of the standard free cash flow to the firm (FCFF) formula using predetermined illustrative inputs, rather than Amazon forecast data.
Input	Value (USD millions unless noted)
EBIT	$1,000.00
Tax rate	20%
Depreciation and amortization	$100.00
Capital expenditures	$250.00
Change in net working capital	$50.00
Formula:  FCFF = EBIT × (1 − tax rate) + depreciation − CapEx − change in net working capital
Expected result:  $1,000 × (1 − 0.20) + $100 − $250 − $50 = $600.00 million.
Observed result:  Executing python test_known_answer.py in the VS Code PowerShell terminal returned FCFF of $600.00 million.
Difference:  $600.00 − $600.00 = $0.00 million.
Outcome:  PASS — observed arithmetic output matched the known answer.
Evidence:  test_known_answer.py; terminal output reproduced below. Optional screenshot: Output/known_answer_test.png, if saved under that exact filename.
AMAZON PROJECT1 — KNOWN-ANSWER FORMULA TEST
Expected FCFF: $600.00 million
Actual FCFF: $600.00 million
Difference: $0.00 million
PASS: Known-answer FCFF calculation
Test scope: This script computes a standalone FCFF formula, rather than invoking the full Amazon forecasting or valuation engine. Consequently, it demonstrates arithmetic agreement for the specified example, not independent end-to-end model validation.
4. AI-OFF Changed-Input Test — CapEx/Revenue
Precommitment recorded:  October 16, 2026, at 3:08 p.m. (user-reported).
Input changed:  CapEx/revenue adjustment from 0.000 to 0.010, equivalent to a 1-percentage-point increase.
Original calculation:  $840,334.00 million projected revenue × 0.010 = $8,403.34 million in additional 2026 CapEx.
Expected capital expenditures:  $168,066.80 million base CapEx + $8,403.34 million = $176,470.14 million.
Predicted direction of related accounts:  2026 ending cash decreases by $8,403.34 million, and ending net PP&E increases by $8,403.34 million, holding the other assumptions fixed.
The originally recorded precommitment should be retained unedited as separate evidence. This section is the clarified post-execution account of the test, and any wording correction made after viewing the model output is not presented as part of the original precommitment.
Observed dashboard results after setting the CapEx/revenue adjustment to 0.010:
2026 metric	Observed amount (USD millions)
Capital expenditures	$176,470.14
Ending cash	$71,894.53
Ending net PP&E	$462,090.14
Primary difference:  $176,470.14 − $176,470.14 = $0.00 million (observed less expected CapEx).
Outcome:  PASS — 2026 observed CapEx matched the precommitted expected CapEx amount. The observed cash and PP&E movements are consistent with the expected $8,403.34 million directional changes.
Dashboard evidence:  Output/ai_off_changed_input_test.png (verify that the file exists and shows the 0.010 input and observed results); preserve additional cash flow and balance sheet screenshots if recorded separately.
Precommitment evidence:  Original time-stamped prediction or unchanged original record retained separately. The dashboard screenshot alone cannot substantiate pre-execution timing or independence.
Scope: This is a targeted assumption-propagation test. It does not verify whether the baseline CapEx assumption, cash-flow treatment, PP&E accounting, or model valuation is economically appropriate.
5. Outstanding Model Limitations and Verification Items
•	The remaining 2026 forecast period and associated partial-year cash flows use preliminary timing assumptions requiring verification against the September 1, 2026 valuation date.
•	Depreciation, stock-based compensation, debt, leases, share dilution, and terminal-period reinvestment are not fully validated or explicitly modeled at the necessary level of detail.
•	The balance-sheet forecast uses simplifying assumptions. A zero aggregate accounting difference demonstrates arithmetic balancing but does not establish accurate account-level forecasting or economic realism.
•	The comparable-company valuation has not been completed or independently reconciled against dated market and filing data.
•	Forecast drivers, terminal growth, WACC inputs, market reference price, and source dates require final verification; scenario mechanics remain simplified.
6. Final Validation Conclusion
Status:  PARTIALLY VALIDATED — MATERIAL MODEL VERIFICATION ITEMS REMAIN OPEN.
The project has documented passing preliminary technical checks, a standalone known-answer FCFF calculation with a zero difference, and a dashboard changed-input CapEx test whose observed 2026 capital expenditures matched the recorded expected amount. These results provide evidence that selected model formulas and dashboard links operate as intended.
The checks do not establish that the full Amazon valuation is independently verified or investment-ready. Outstanding items include detailed financial-statement modeling, valuation assumptions and timing, share count, debt and lease treatment, source reconciliation, and completion of comparable-company analysis. The valuation and any investment conclusion should therefore be described as preliminary, with limitations disclosed in the accompanying decision memo and research record.
7. Evidence and Reproducibility Index
File / record	Purpose
test_known_answer.py	Reproduce $600.00 million FCFF arithmetic check
Output/known_answer_test.png (if saved)	Optional screenshot of passing terminal output
Output/ai_off_changed_input_test.png	CapEx/revenue 0.010 dashboard changed-input result
Original October 16 precommitment	Preserve original expectation and timestamp separately
Model test scripts and dashboard code	Supporting development checks and interactive test
Evidence paths refer to files in the project repository. Before submission, confirm each referenced file exists and opens; remove or correct any optional path that does not exist. This record contains no claim that all outstanding financial or market-source verification has been completed.
