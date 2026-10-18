# Amazon Interactive Dashboard Test Log

Date tested: October 16, 2026
Application: Streamlit Amazon Valuation Dashboard

## Test 1: Operating Margin
Action: Increase operating margin by 1 percentage point.
Observed result: Estimated value per share increased.
Status: PASS

## Test 2: Capital Expenditures
Action: Increase CapEx/revenue by 1 percentage point.
Observed result: Estimated value per share decreased.
Status: PASS

## Test 3: Reset
Action: Click Reset to base case.
Observed result: Valuation returned to approximately $105.28.
Status: PASS

## Limitations
These are interactive directional checks, not independent
financial-model verification. The current valuation remains
preliminary, and additional source, timing, accounting,
and sensitivity validation is required.
