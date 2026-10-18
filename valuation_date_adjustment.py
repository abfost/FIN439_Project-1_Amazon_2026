# Amazon preliminary valuation-date timing adjustment
# Valuation date: September 1, 2026
# All amounts are USD millions

from datetime import date
from free_cash_flow import fcff_forecast
from wacc import wacc

valuation_date = date(2026, 9, 1)
terminal_growth = 0.03

def discount_years(target_date):
    return (target_date - valuation_date).days / 365.25

# NOTE:
# 2026 full-year FCFF includes January-August cash flows.
# We cannot simply discount all of it from September 1.
# This model temporarily assumes monthly-even FCFF.
# The actual stub period needs an operating forecast.

remaining_2026_fraction = 4 / 12
remaining_2026_fcff = fcff_forecast[2026] * remaining_2026_fraction

adjusted_fcff = {
    2026: remaining_2026_fcff,
    2027: fcff_forecast[2027],
    2028: fcff_forecast[2028],
    2029: fcff_forecast[2029],
    2030: fcff_forecast[2030],
}

present_value_fcff = 0

print("\nAMAZON SEPTEMBER 1, 2026 DCF TIMING ADJUSTMENT")
print("All amounts in USD millions")

for year in range(2026, 2031):
    year_end = date(year, 12, 31)
    years_to_discount = discount_years(year_end)

    pv = adjusted_fcff[year] / (1 + wacc) ** years_to_discount
    present_value_fcff += pv

    print(f"{year}: FCFF ${adjusted_fcff[year]:,.2f}M; "
          f"PV ${pv:,.2f}M; t={years_to_discount:.3f}")

terminal_value = (
    fcff_forecast[2030] * (1 + terminal_growth)
    / (wacc - terminal_growth)
)

pv_terminal_value = terminal_value / (
    (1 + wacc) ** discount_years(date(2030, 12, 31))
)

adjusted_enterprise_value = (
    present_value_fcff + pv_terminal_value
)

print(f"\nAdjusted PV of FCFF: ${present_value_fcff:,.2f} million")
print(f"Adjusted PV of Terminal Value: ${pv_terminal_value:,.2f} million")
print(f"Adjusted Enterprise Value: ${adjusted_enterprise_value:,.2f} million")

assert wacc > terminal_growth
assert adjusted_enterprise_value > 0

print("\nPASS: Preliminary valuation-date adjustment calculated")
print("WARNING: 2026 stub cash flow still requires refinement.")