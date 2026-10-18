# Amazon capital expenditure forecast
# All figures in USD millions

from revenue_forecast import five_year_forecast

capex_assumptions = {
    2026: 0.20,
    2027: 0.19,
    2028: 0.18,
    2029: 0.17,
    2030: 0.16,
}

capex_forecast = {}

print("\nAMAZON CAPITAL EXPENDITURE FORECAST")
print("All figures in USD millions")

for year in range(2026, 2031):
    revenue = sum(five_year_forecast[year].values())
    capex = revenue * capex_assumptions[year]

    capex_forecast[year] = capex

    print(f"\n{year}")
    print(f"  Revenue: ${revenue:,.2f} million")
    print(f"  CapEx Assumption: {capex_assumptions[year]:.2%}")
    print(f"  Forecast CapEx: ${capex:,.2f} million")