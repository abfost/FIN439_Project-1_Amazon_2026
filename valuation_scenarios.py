# Amazon preliminary DCF valuation scenarios
# September 1, 2026 timing convention
# All financial values in USD millions

from datetime import date
from free_cash_flow import fcff_forecast
from wacc import wacc

valuation_date = date(2026, 9, 1)

scenarios = {
    "Low": {
        "wacc": wacc + 0.01,
        "growth": 0.02,
        "fcff_multiplier": 0.80,
    },
    "Base": {
        "wacc": wacc,
        "growth": 0.03,
        "fcff_multiplier": 1.00,
    },
    "High": {
        "wacc": wacc - 0.01,
        "growth": 0.04,
        "fcff_multiplier": 1.20,
    },
}

# Latest reported June 2026 bridge inputs
debt = 128894
cash = 78213
marketable_securities = 44775
shares = 10783
reference_price = 254.92

def years_until(target_date):
    return (target_date - valuation_date).days / 365.25

def calculate_scenario(inputs):
    rate = inputs["wacc"]
    growth = inputs["growth"]
    multiplier = inputs["fcff_multiplier"]

    if rate <= growth:
        raise ValueError("WACC must exceed terminal growth")

    pv_fcff = 0

    for year in range(2026, 2031):
        forecast = fcff_forecast[year] * multiplier

        if year == 2026:
            forecast *= 4 / 12

        t = years_until(date(year, 12, 31))
        pv_fcff += forecast / (1 + rate) ** t

    terminal_fcff = fcff_forecast[2030] * multiplier

    terminal_value = (
        terminal_fcff * (1 + growth) / (rate - growth)
    )

    pv_terminal = terminal_value / (
        (1 + rate) ** years_until(date(2030, 12, 31))
    )

    enterprise_value = pv_fcff + pv_terminal
    equity_value = enterprise_value - debt + cash + marketable_securities
    per_share = equity_value / shares

    return enterprise_value, equity_value, per_share


print("\nAMAZON PRELIMINARY VALUATION SCENARIOS")

scenario_results = {}

for name, assumptions in scenarios.items():
    ev, equity, price = calculate_scenario(assumptions)

    scenario_results[name] = {
        "enterprise_value": ev,
        "equity_value": equity,
        "per_share": price,
    }

    print(f"\n{name} Case")
    print(f"  WACC: {assumptions['wacc']:.2%}")
    print(f"  Terminal Growth: {assumptions['growth']:.2%}")
    print(f"  Enterprise Value: ${ev:,.2f} million")
    print(f"  Value Per Share: ${price:,.2f}")
    print(f"  Upside/Downside: {price / reference_price - 1:.2%}")

assert (
    scenario_results["Low"]["per_share"]
    < scenario_results["Base"]["per_share"]
    < scenario_results["High"]["per_share"]
)

print("\nPASS: Low, base, and high scenarios calculated")