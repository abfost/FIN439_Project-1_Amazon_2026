
# Amazon.com, Inc. (AMZN) — FIN 43900 Project 1

## Project Overview

This project develops a preliminary corporate valuation and interactive financial analysis application for Amazon.com, Inc. (AMZN).

**Valuation date:** September 1, 2026  
**Currency:** USD, with financial statement amounts generally reported in millions  
**Investment decision:** WATCH / DEFER  
**Intended user:** Buy-side investment committee evaluating whether to initiate an Amazon position.

The model is preliminary and has not been fully independently validated.

## Investment Conclusion

The preliminary discounted cash flow analysis estimates Amazon's equity value at approximately $105 per share, compared with a reference market price of $254.92.

Sensitivity cases produce an illustrative valuation range of approximately $66.00–$171.90 per share.

These values depend on assumptions concerning AWS growth, operating profitability, capital expenditures, working capital, WACC, and terminal growth. Outstanding model limitations prevent treating the results as a definitive investment recommendation.

## Application

The project includes a Streamlit dashboard with adjustable assumptions for:

- Weighted average cost of capital (WACC)
- Terminal growth rate
- Operating margin
- Capital expenditures as a percentage of revenue

The dashboard displays valuation results, forecast cash flows, preliminary financial statements, and selected validation checks.

### Running the Dashboard

Install Python and the project dependencies.

From the project folder, run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal. Open that address in a browser.

## Financial Analysis

The Python model includes:

- Amazon historical financial inputs
- Five-year segment revenue forecasts
- Operating-income projections
- Preliminary income statement, balance sheet, and cash flow forecasts
- Working-capital and fixed-asset schedules
- Discounted free cash flow valuation
- WACC and terminal-value calculations
- Sensitivity and reverse-DCF analyses
- Preliminary comparable-company valuation

### Comparable-Company Analysis

The project uses Walmart, Microsoft, and Alphabet as preliminary comparison companies.

| Company | EV/Revenue | P/E |
|---|---:|---:|
| Walmart | 1.19x | 38.07x |
| Microsoft | 11.12x | 27.82x |
| Alphabet | 8.87x | 16.78x |

These multiples are illustrative and require further reconciliation of cash, debt, share counts, and earnings definitions.

The supporting data and calculations are in:

- `Data/peer_valuation_inputs.csv`
- `Data/peer_valuation_results.csv`
- `peer_valuation.py`

## Validation

Development checks include a $600 million standalone known-answer FCFF test, five valuation arithmetic tests, preliminary five-year statement-linkage tests, and a changed-input CapEx sensitivity test.

A separate dashboard demonstration illustrates the invalid case in which terminal growth equals WACC. This is a hypothetical validation demonstration rather than a test that passes an invalid assumption through the complete valuation engine.

To run selected checks:

```bash
python test_known_answer.py
python test_valuation_engine.py
python test_three_statements.py
```

See `cold_run_log.md` and the Validation and AI Use Record for further details.

## Supporting Materials

- `Edition_A/` — Original research checkpoint materials
- `Edition_B/` — Updated research
- `Docs/` — Investment decision memo
- `Data/` — Financial inputs and peer valuation results
- `Output/` — Generated analysis and validation evidence
- `Submission/` — Final submission documents, where available

## Limitations

The application is a preliminary valuation tool. Important unresolved items include the September 2026 partial-year cash flow treatment, depreciation and stock-based compensation, debt and lease classification, diluted share count, terminal reinvestment, and full account-level financial-statement forecasting.

The comparable-company analysis uses preliminary screening multiples rather than a fully standardized independent valuation.

The code and its automated checks do not establish that the complete valuation is economically accurate or investment-ready.

## AI Use

ChatGPT assisted extensively with coding, debugging, model development, explanations, and written documentation. The author is responsible for reviewing the analysis and interpreting the financial results. See the separate Validation and AI Use Record for the full disclosure.
