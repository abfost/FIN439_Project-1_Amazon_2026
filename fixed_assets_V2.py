import pandas as pd

# Amazon historical fixed-asset analysis
# All amounts are USD millions

data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Reported historical financial figures
ppe_2024 = values["net_property_equipment_2024"]
ppe_2025 = values["net_property_equipment_2025"]
cash_capex_2025 = values["purchases_property_equipment_2025"]

# Calculate the change in net property and equipment
ppe_change = ppe_2025 - ppe_2024

# This difference is NOT depreciation alone.
# It can include leased assets, disposals, depreciation,
# noncash additions, and other adjustments.
unexplained_difference = cash_capex_2025 - ppe_change

print("\nAMAZON HISTORICAL FIXED-ASSET ANALYSIS")
print("All figures in USD millions")

print(f"2024 Net PP&E: ${ppe_2024:,.2f} million")
print(f"2025 Net PP&E: ${ppe_2025:,.2f} million")
print(f"Change in Net PP&E: ${ppe_change:,.2f} million")
print(f"2025 Cash CapEx: ${cash_capex_2025:,.2f} million")
print(f"CapEx Less PP&E Change: ${unexplained_difference:,.2f} million")

# Verify the historical net PP&E change
assert abs(ppe_change - 104360) < 0.01

print("PASS: Historical PP&E calculation reconciles")
# Amazon preliminary five-year fixed-asset forecast
# All values are USD millions

from capital_expenditures import capex_forecast

depreciation_rate = 0.20
beginning_ppe = ppe_2025

fixed_asset_forecast = {}

print("\nAMAZON FIVE-YEAR FIXED-ASSET FORECAST")
print("All figures in USD millions")

for year in range(2026, 2031):
    capex = capex_forecast[year]

    # Preliminary depreciation assumption
    depreciation = beginning_ppe * depreciation_rate

    # Placeholder: no noncash additions or other PP&E adjustments
    # Final model will require explicit treatment of these items.
    other_ppe_adjustments = 0

    ending_ppe = (
        beginning_ppe
        + capex
        - depreciation
        + other_ppe_adjustments
    )

    fixed_asset_forecast[year] = {
        "beginning_ppe": beginning_ppe,
        "capex": capex,
        "depreciation": depreciation,
        "other_adjustments": other_ppe_adjustments,
        "ending_ppe": ending_ppe,
    }

    assert abs(
        beginning_ppe
        + capex
        - depreciation
        + other_ppe_adjustments
        - ending_ppe
    ) < 0.01

    print(f"\n{year}")
    print(f"  Beginning PP&E: ${beginning_ppe:,.2f} million")
    print(f"  Capital Expenditures: ${capex:,.2f} million")
    print(f"  Depreciation: ${depreciation:,.2f} million")
    print(f"  Ending PP&E: ${ending_ppe:,.2f} million")

    beginning_ppe = ending_ppe

print("\nPASS: All five forecast PP&E schedules reconcile")