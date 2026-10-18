import pandas as pd

# Load Amazon's historical financial data
data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Calculate revenue growth
growth_2024 = values["revenue_2024"] / values["revenue_2023"] - 1
growth_2025 = values["revenue_2025"] / values["revenue_2024"] - 1

# Calculate operating profit margins
margin_2023 = values["operating_income_2023"] / values["revenue_2023"]
margin_2024 = values["operating_income_2024"] / values["revenue_2024"]
margin_2025 = values["operating_income_2025"] / values["revenue_2025"]

print(f"2024 Revenue Growth: {growth_2024:.2%}")
print(f"2025 Revenue Growth: {growth_2025:.2%}")

print(f"2023 Operating Margin: {margin_2023:.2%}")
print(f"2024 Operating Margin: {margin_2024:.2%}")
print(f"2025 Operating Margin: {margin_2025:.2%}")
# Calculate historical growth for each Amazon segment
segments = ["north_america", "international", "aws"]

print("\nAmazon Segment Revenue Growth")

for segment in segments:
    revenue_2023 = values[f"{segment}_revenue_2023"]
    revenue_2024 = values[f"{segment}_revenue_2024"]
    revenue_2025 = values[f"{segment}_revenue_2025"]

    growth_2024 = revenue_2024 / revenue_2023 - 1
    growth_2025 = revenue_2025 / revenue_2024 - 1

    print(
        f"{segment}: "
        f"2024 Growth = {growth_2024:.2%}, "
        f"2025 Growth = {growth_2025:.2%}"
    )
    # Compare first-half 2026 segment sales with first-half 2025
print("\nFirst-Half 2026 Revenue Growth")

for segment in ["north_america", "international", "aws", "consolidated"]:
    revenue_2025 = values[f"{segment}_h1_revenue_2025"]
    revenue_2026 = values[f"{segment}_h1_revenue_2026"]

    growth = revenue_2026 / revenue_2025 - 1

    print(f"{segment}: {growth:.2%}")
   # Calculate historical operating margins for Amazon segments
print("\nAmazon Historical Segment Operating Margins")

for segment in ["north_america", "international", "aws"]:
    print(f"\n{segment}")

    for year in [2023, 2024, 2025]:
        revenue = values[f"{segment}_revenue_{year}"]
        operating_income = values[f"{segment}_operating_income_{year}"]

        margin = operating_income / revenue

        print(f"  {year}: {margin:.2%}") 
        # Calculate first-half operating margins for Amazon segments
print("\nAmazon First-Half Operating Margins")

for segment in ["north_america", "international", "aws"]:
    print(f"\n{segment}")

    for year in [2025, 2026]:
        revenue = values[f"{segment}_h1_revenue_{year}"]
        operating_income = values[f"{segment}_h1_operating_income_{year}"]

        margin = operating_income / revenue

        print(f"  H1 {year}: {margin:.2%}")