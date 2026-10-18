# Amazon preliminary discounted cash flow valuation
# All financial values in USD millions

from free_cash_flow import fcff_forecast
from wacc import wacc

# Preliminary perpetual growth assumption
terminal_growth_rate = 0.03

assert wacc > terminal_growth_rate, (
    "WACC must exceed terminal growth rate"
)

# Discount each year's FCFF
present_value_fcff = 0

print("\nAMAZON PRELIMINARY DCF VALUATION")
print("All financial values in USD millions")

for year in range(2026, 2031):
    period = year - 2025
    fcff = fcff_forecast[year]

    discount_factor = (1 + wacc) ** period
    present_value = fcff / discount_factor

    present_value_fcff += present_value

    print(f"\n{year}")
    print(f"  FCFF: ${fcff:,.2f} million")
    print(f"  Present Value: ${present_value:,.2f} million")

# Calculate terminal value at end of 2030
fcff_2030 = fcff_forecast[2030]
fcff_2031 = fcff_2030 * (1 + terminal_growth_rate)

terminal_value = fcff_2031 / (wacc - terminal_growth_rate)
present_value_terminal = terminal_value / (1 + wacc) ** 5

# Enterprise value
enterprise_value = present_value_fcff + present_value_terminal

print("\nDCF RESULTS")
print(f"Present Value of Forecast FCFF: ${present_value_fcff:,.2f} million")
print(f"Terminal Growth Rate: {terminal_growth_rate:.2%}")
print(f"Terminal Value: ${terminal_value:,.2f} million")
print(f"Present Value of Terminal Value: ${present_value_terminal:,.2f} million")
print(f"Preliminary Enterprise Value: ${enterprise_value:,.2f} million")

assert enterprise_value > 0

print("\nPASS: Preliminary DCF valuation calculated")