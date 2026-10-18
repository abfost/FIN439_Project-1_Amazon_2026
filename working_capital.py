import pandas as pd

# Load historical Amazon financial data
data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

print("AMAZON HISTORICAL OPERATING NET WORKING CAPITAL")
print("All figures in USD millions")

working_capital = {}

for year in [2024, 2025]:
    inventory = values[f"inventory_{year}"]
    receivables = values[f"receivables_other_{year}"]
    payables = values[f"accounts_payable_{year}"]
    accrued = values[f"accrued_expenses_other_{year}"]
    unearned = values[f"unearned_revenue_{year}"]

    nwc = inventory + receivables - payables - accrued - unearned
    working_capital[year] = nwc

    print(f"{year} Operating NWC: ${nwc:,.2f} million")

change_in_nwc = working_capital[2025] - working_capital[2024]

print(f"\n2025 Change in Operating NWC: ${change_in_nwc:,.2f} million")

assert working_capital[2024] == -79766
assert working_capital[2025] == -111951

print("PASS: Historical operating NWC calculations reconcile")
# Preliminary forecast of operating net working capital
# Assumption: Operating NWC equals -14% of forecast revenue

from revenue_forecast import five_year_forecast

forecast_nwc_ratio = -0.14
previous_nwc = working_capital[2025]

forecast_working_capital = {}

print("\nAMAZON FORECAST OPERATING NET WORKING CAPITAL")
print("All figures in USD millions")

for year in range(2026, 2031):
    revenue = sum(five_year_forecast[year].values())

    forecast_nwc = revenue * forecast_nwc_ratio
    change_in_nwc = forecast_nwc - previous_nwc

    forecast_working_capital[year] = {
        "revenue": revenue,
        "operating_nwc": forecast_nwc,
        "change_in_nwc": change_in_nwc,
    }

    print(f"\n{year}")
    print(f"  Revenue: ${revenue:,.2f} million")
    print(f"  Operating NWC: ${forecast_nwc:,.2f} million")
    print(f"  Change in NWC: ${change_in_nwc:,.2f} million")

    previous_nwc = forecast_nwc