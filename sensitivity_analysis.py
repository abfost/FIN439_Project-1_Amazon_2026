# Amazon preliminary DCF sensitivity analysis
# All enterprise values are in USD billions
# Uses the existing preliminary 2025 year-end valuation convention

from free_cash_flow import fcff_forecast
from wacc import wacc

def calculate_enterprise_value(discount_rate, terminal_growth):
    if discount_rate <= terminal_growth:
        raise ValueError("WACC must exceed terminal growth")

    pv_cash_flows = sum(
        fcff_forecast[year] / (1 + discount_rate) ** (year - 2025)
        for year in range(2026, 2031)
    )

    terminal_value = (
        fcff_forecast[2030] * (1 + terminal_growth)
        / (discount_rate - terminal_growth)
    )

    pv_terminal_value = terminal_value / (1 + discount_rate) ** 5

    return pv_cash_flows + pv_terminal_value


wacc_values = [wacc - 0.02, wacc - 0.01, wacc,
               wacc + 0.01, wacc + 0.02]

growth_values = [0.02, 0.025, 0.03, 0.035, 0.04]

print("\nAMAZON DCF SENSITIVITY ANALYSIS")
print("Enterprise values in USD billions")
print("Rows = WACC; columns = terminal growth\n")

header = "WACC / Growth" + "".join(
    f"{g * 100:>12.1f}%" for g in growth_values
)
print(header)

for discount_rate in wacc_values:
    row = f"{discount_rate * 100:>12.2f}%"
    for growth in growth_values:
        ev_billions = (
            calculate_enterprise_value(discount_rate, growth) / 1000
        )
        row += f"{ev_billions:>13,.2f}"
    print(row)

# Known-answer comparison against the previous DCF run
base_ev = calculate_enterprise_value(wacc, 0.03)
assert abs(base_ev - 1059168.40) < 1.0, (
    "Base valuation differs from expected DCF result"
)

# Real directional test using the valuation function
assert (
    calculate_enterprise_value(wacc - 0.01, 0.03)
    > calculate_enterprise_value(wacc, 0.03)
)

assert (
    calculate_enterprise_value(wacc, 0.04)
    > calculate_enterprise_value(wacc, 0.03)
)

print("\nPASS: DCF sensitivity and directional checks completed")