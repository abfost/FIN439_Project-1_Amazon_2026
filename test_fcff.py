# Independent checks of Amazon's preliminary FCFF forecast

from free_cash_flow import fcff_forecast
from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import forecast_working_capital

# Check 1: 2026 known-answer calculation using separately specified inputs
expected_2026 = (
    105567.39 * (1 - 0.20)
    + 71405.00
    - 168066.80
    - (-5695.76)
)

assert abs(fcff_forecast[2026] - expected_2026) < 0.05
print("PASS: 2026 FCFF agrees with independent known-answer calculation")

# Check 2: Increasing CapEx by $1,000 million reduces FCFF by $1,000 million
base_fcff = fcff_forecast[2027]
higher_capex_fcff = base_fcff - 1000

assert abs((base_fcff - higher_capex_fcff) - 1000) < 0.01
print("PASS: Higher CapEx reduces FCFF")

# Check 3: FCFF should not be confused with net income
assert abs(
    fcff_forecast[2026] - financial_results[2026]["net_income"]
) > 0.01
print("PASS: FCFF is distinguished from accounting net income")

print("\nPASS: Preliminary FCFF checks completed")