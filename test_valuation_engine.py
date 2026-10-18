
"""Five arithmetic checks for the preliminary Amazon valuation engine."""

from datetime import date

from analysis import (
    run_analysis,
    BASE_FCFF,
    REVENUE,
    DEFAULTS,
    VALUATION_DATE,
    values,
)

# Obtain the same filing inputs used by the valuation engine.
cash = float(values["cash_and_equivalents_2026_q2"])
marketable_securities = float(
    values["marketable_securities_2026_q2"]
)
debt = float(values["long_term_debt_carrying_2026_q2"])
shares = float(values["shares_outstanding_2026_q2"])

base = run_analysis({})

# TEST 1: Operating margin and FCFF.
revenue_2030 = REVENUE[2030]

higher_margin = run_analysis({
    "operating_margin_change": 0.01
})

expected_fcff_2030 = (
    BASE_FCFF[2030] + revenue_2030 * 0.01 * 0.80
)

actual_fcff_2030 = higher_margin["forecast"][2030]["fcff"]

assert abs(actual_fcff_2030 - expected_fcff_2030) < 0.01
print("PASS 1: Operating margin calculation")


# TEST 2: Capital expenditures and FCFF.
# Test the immediate effect in 2026, before the higher
# CapEx changes depreciation in subsequent years.

higher_capex = run_analysis({
    "capex_rate_change": 0.01
})

revenue_2026 = REVENUE[2026]

expected_fcff_2026 = (
    BASE_FCFF[2026] - revenue_2026 * 0.01
)

actual_fcff_2026 = higher_capex["forecast"][2026]["fcff"]

assert abs(actual_fcff_2026 - expected_fcff_2026) < 0.01, (
    f"Expected {expected_fcff_2026:.2f}, "
    f"observed {actual_fcff_2026:.2f}"
)

print("PASS 2: Immediate 2026 CapEx calculation")

# TEST 3: Enterprise-to-equity valuation bridge.
expected_equity = (
    base["enterprise_value"]
    - debt
    + cash
    + marketable_securities
)

assert abs(
    base["equity_value"] - expected_equity
) < 0.01

expected_share_value = expected_equity / shares

assert abs(
    base["value_per_share"] - expected_share_value
) < 0.000001

print("PASS 3: Equity-value bridge")

# TEST 4: Discounting of forecast FCFF.
wacc = DEFAULTS["wacc"]

time_2028 = (
    date(2028, 12, 31) - VALUATION_DATE
).days / 365.25

expected_2028_pv = (
    BASE_FCFF[2028] / (1 + wacc) ** time_2028
)

actual_2028_pv = base["forecast"][2028]["discounted_fcff"]

assert abs(actual_2028_pv - expected_2028_pv) < 0.01

print("PASS 4: Discounting calculation")

# TEST 5: Terminal value.
growth = DEFAULTS["terminal_growth"]

terminal_value = (
    BASE_FCFF[2030] * (1 + growth) / (wacc - growth)
)

time_2030 = (
    date(2030, 12, 31) - VALUATION_DATE
).days / 365.25

expected_pv_terminal = (
    terminal_value / (1 + wacc) ** time_2030
)

assert abs(
    base["pv_terminal"] - expected_pv_terminal
) < 0.01

print("PASS 5: Terminal-value calculation")

print(
    "\nPASS: Five preliminary valuation arithmetic "
    "checks completed"
)
