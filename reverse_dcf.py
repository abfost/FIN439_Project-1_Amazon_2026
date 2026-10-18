# Amazon preliminary reverse DCF
# Find the FCFF multiplier needed to justify market price

from valuation_scenarios import calculate_scenario, scenarios
from wacc import share_price

shares = 10783
market_price = share_price

# Keep base WACC and terminal growth unchanged
base_assumptions = scenarios["Base"].copy()

# Current model valuation
base_ev, base_equity, base_price = calculate_scenario(
    base_assumptions
)

# Determine the multiplier using the actual valuation function
low = 0.0
high = 10.0

for _ in range(100):
    midpoint = (low + high) / 2

    test_assumptions = base_assumptions.copy()
    test_assumptions["fcff_multiplier"] = midpoint

    ev, equity, price = calculate_scenario(test_assumptions)

    if price < market_price:
        low = midpoint
    else:
        high = midpoint

required_multiplier = (low + high) / 2
required_increase = (required_multiplier - 1) * 100

final_assumptions = base_assumptions.copy()
final_assumptions["fcff_multiplier"] = required_multiplier

ev, equity, implied_price = calculate_scenario(final_assumptions)

print("\nAMAZON PRELIMINARY REVERSE DCF")
print(f"Reference Market Price: ${market_price:,.2f}")
print(f"Base Model Value Per Share: ${base_price:,.2f}")
print(f"Required FCFF Multiplier: {required_multiplier:.2f}x")
print(f"Required FCFF Increase: {required_increase:.2f}%")
print(f"Reverse DCF Implied Price: ${implied_price:,.2f}")

assert abs(implied_price - market_price) < 0.01

print("\nPASS: Reverse DCF matches reference market price")
print("NOTE: This scales FCFF, not individual business drivers.")