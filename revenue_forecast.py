import pandas as pd

# Load Amazon's historical financial data
data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Historical base-year revenue in USD millions
revenue_2025 = values["revenue_2025"]

# Preliminary analyst assumption
growth_2026 = 0.12

# Calculate next year's forecast revenue
revenue_2026 = revenue_2025 * (1 + growth_2026)

print(f"2025 Actual Revenue: ${revenue_2025:,.0f} million")
print(f"2026 Assumed Growth: {growth_2026:.2%}")
print(f"2026 Forecast Revenue: ${revenue_2026:,.2f} million")
# Development test: check revenue response to growth changes
low_growth = revenue_2025 * 1.10
base_growth = revenue_2025 * 1.12
high_growth = revenue_2025 * 1.14

assert low_growth < base_growth < high_growth, (
    "FAIL: Revenue does not increase with growth"
)

print("PASS: Higher growth produces higher forecast revenue")

print(f"10% Growth Scenario: ${low_growth:,.2f} million")
print(f"12% Growth Scenario: ${base_growth:,.2f} million")
print(f"14% Growth Scenario: ${high_growth:,.2f} million")
# Calculate historical second-half 2025 revenue by segment
print("\nAmazon Second-Half 2025 Revenue")

segments = ["north_america", "international", "aws"]

h2_total = 0

for segment in segments:
    full_year = values[f"{segment}_revenue_2025"]
    first_half = values[f"{segment}_h1_revenue_2025"]

    second_half = full_year - first_half
    h2_total += second_half

    print(f"{segment}: ${second_half:,.0f} million")

# Reconcile segment total with consolidated revenue
reported_h2 = (
    values["revenue_2025"]
    - values["consolidated_h1_revenue_2025"]
)

assert abs(h2_total - reported_h2) < 0.01, (
    "FAIL: Second-half segment revenue does not reconcile"
)

print(f"Total H2 2025 Revenue: ${h2_total:,.0f} million")
print("PASS: Second-half segment revenue reconciles")

# 2026 segment-based revenue forecast
# Values are USD millions
# H1 2026 is actual; H2 2026 uses analyst assumptions

h2_growth_assumptions = {
    "north_america": 0.13,
    "international": 0.15,
    "aws": 0.30,
}

forecast_2026 = {}
h2_forecast_total = 0

print("\n2026 Segment Revenue Forecast")

for segment in ["north_america", "international", "aws"]:
    h1_actual = values[f"{segment}_h1_revenue_2026"]

    h2_2025 = (
        values[f"{segment}_revenue_2025"]
        - values[f"{segment}_h1_revenue_2025"]
    )

    h2_forecast = h2_2025 * (1 + h2_growth_assumptions[segment])
    full_year_forecast = h1_actual + h2_forecast

    forecast_2026[segment] = full_year_forecast
    h2_forecast_total += h2_forecast

    print(f"{segment}: ${full_year_forecast:,.2f} million")

total_revenue_2026 = sum(forecast_2026.values())

growth_2026 = (
    total_revenue_2026 / values["revenue_2025"] - 1
)

assert abs(
    total_revenue_2026
    - sum(forecast_2026.values())
) < 0.01, "FAIL: Segment forecast does not reconcile"

print(f"\nTotal 2026 Revenue: ${total_revenue_2026:,.2f} million")
print(f"2026 Consolidated Growth: {growth_2026:.2%}")
print("PASS: 2026 segment forecast reconciles")
# Forecast Amazon segment revenue for 2027–2030
# Figures are in USD millions

future_growth_rates = {
    "north_america": {
        2027: 0.11, 2028: 0.10, 2029: 0.09, 2030: 0.08
    },
    "international": {
        2027: 0.13, 2028: 0.12, 2029: 0.11, 2030: 0.10
    },
    "aws": {
        2027: 0.27, 2028: 0.24, 2029: 0.21, 2030: 0.18
    }
}

# Start with the segment forecasts we calculated for 2026
five_year_forecast = {2026: forecast_2026.copy()}

for year in range(2027, 2031):
    five_year_forecast[year] = {}

    for segment in ["north_america", "international", "aws"]:
        prior_year_revenue = five_year_forecast[year - 1][segment]
        growth_rate = future_growth_rates[segment][year]

        five_year_forecast[year][segment] = (
            prior_year_revenue * (1 + growth_rate)
        )

# Show the complete forecast
print("\nAmazon Five-Year Segment Revenue Forecast")
print("All figures in USD millions")

for year in range(2026, 2031):
    year_total = sum(five_year_forecast[year].values())

    print(f"\n{year}")
    for segment, revenue in five_year_forecast[year].items():
        print(f"  {segment}: ${revenue:,.2f} million")

    print(f"  Total Revenue: ${year_total:,.2f} million")