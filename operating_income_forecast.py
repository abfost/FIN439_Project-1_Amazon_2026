import pandas as pd

# Load Amazon's historical financial data
data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Preliminary forecast revenue from the segment model
# All figures are USD millions
# Use the revenue model rather than copied forecast numbers
from revenue_forecast import five_year_forecast

revenue_forecast = five_year_forecast

# Preliminary operating-margin assumptions
operating_margins = {
    "north_america": {2026: 0.075, 2027: 0.077, 2028: 0.079, 2029: 0.080, 2030: 0.080},
    "international": {2026: 0.036, 2027: 0.038, 2028: 0.040, 2029: 0.042, 2030: 0.045},
    "aws": {2026: 0.370, 2027: 0.370, 2028: 0.365, 2029: 0.360, 2030: 0.355},
}

# Calculate operating income by segment and year
print("Amazon Five-Year Operating Income Forecast")
print("All figures in USD millions")

for year in range(2026, 2031):
    total_operating_income = 0
    total_revenue = 0

    print(f"\n{year}")

    for segment in ["north_america", "international", "aws"]:
        revenue = revenue_forecast[year][segment]
        margin = operating_margins[segment][year]

        operating_income = revenue * margin

        total_operating_income += operating_income
        total_revenue += revenue

        print(f"  {segment}: ${operating_income:,.2f} million")

    consolidated_margin = total_operating_income / total_revenue

    print(f"  Total Operating Income: ${total_operating_income:,.2f} million")
    print(f"  Consolidated Operating Margin: {consolidated_margin:.2%}")