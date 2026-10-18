import pandas as pd

from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import forecast_working_capital

data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Check the reported 2025 balance sheet
assets_2025 = values["total_assets_2025"]
liabilities_2025 = values["total_liabilities_2025"]
equity_2025 = values["total_equity_2025"]

historical_difference = (
    assets_2025 - liabilities_2025 - equity_2025
)

assert abs(historical_difference) < 0.01
print("PASS: 2025 reported balance sheet balances")

# Build a preliminary indirect operating cash flow bridge.
# Other noncash adjustments and financing activities
# remain to be modeled and validated.
print("\nAMAZON PRELIMINARY CASH FLOW BRIDGE")
print("All figures in USD millions")

cash_flow_bridge = {}

for year in range(2026, 2031):
    net_income = financial_results[year]["net_income"]
    depreciation = fixed_asset_forecast[year]["depreciation"]
    capex = fixed_asset_forecast[year]["capex"]
    change_nwc = forecast_working_capital[year]["change_in_nwc"]

    preliminary_operating_cash_flow = (
        net_income + depreciation - change_nwc
    )

    preliminary_cash_after_capex = (
        preliminary_operating_cash_flow - capex
    )

    cash_flow_bridge[year] = {
        "net_income": net_income,
        "depreciation": depreciation,
        "change_nwc": change_nwc,
        "operating_cash_flow": preliminary_operating_cash_flow,
        "capex": capex,
        "cash_after_capex": preliminary_cash_after_capex,
    }

    print(f"\n{year}")
    print(f"  Net Income: ${net_income:,.2f} million")
    print(f"  Depreciation: ${depreciation:,.2f} million")
    print(f"  Change in NWC: ${change_nwc:,.2f} million")
    print(
        f"  Preliminary Operating Cash Flow: "
        f"${preliminary_operating_cash_flow:,.2f} million"
    )
    print(f"  Capital Expenditures: ${capex:,.2f} million")
    print(
        f"  Preliminary Cash After CapEx: "
        f"${preliminary_cash_after_capex:,.2f} million"
    )

print("\nPASS: Preliminary cash flow bridge calculated")

# Check whether our historical asset accounts reconcile
print("\nAMAZON 2025 BALANCE SHEET ACCOUNT CHECKS")

current_assets = (
    values["cash_and_equivalents_2025"]
    + values["marketable_securities_2025"]
    + values["inventory_2025"]
    + values["receivables_other_2025"]
)

reported_current_assets = values["total_current_assets_2025"]

assert abs(current_assets - reported_current_assets) < 0.01
print("PASS: 2025 current assets reconcile")

current_liabilities = (
    values["accounts_payable_2025"]
    + values["accrued_expenses_other_2025"]
    + values["unearned_revenue_2025"]
)

reported_current_liabilities = values["total_current_liabilities_2025"]

assert abs(current_liabilities - reported_current_liabilities) < 0.01
print("PASS: 2025 current liabilities reconcile")
# Verify 2025 detailed asset balances
print("\nAMAZON 2025 DETAILED BALANCE SHEET CHECK")

calculated_assets = (
    values["total_current_assets_2025"]
    + values["net_property_equipment_2025"]
    + values["operating_lease_assets_2025"]
    + values["goodwill_2025"]
    + values["other_noncurrent_assets_2025"]
)

reported_assets = values["total_assets_2025"]

asset_difference = calculated_assets - reported_assets

print(f"Calculated Assets: ${calculated_assets:,.2f} million")
print(f"Reported Assets: ${reported_assets:,.2f} million")
print(f"Difference: ${asset_difference:,.2f} million")

assert abs(asset_difference) < 0.01, "Detailed 2025 assets do not reconcile"

print("PASS: 2025 detailed assets reconcile")
# Verify Amazon's detailed 2025 liabilities and equity
print("\nAMAZON 2025 LIABILITIES AND EQUITY CHECK")

calculated_liabilities = (
    values["total_current_liabilities_2025"]
    + values["long_term_lease_liabilities_2025"]
    + values["long_term_debt_carrying_2025"]
    + values["other_long_term_liabilities_2025"]
)

reported_liabilities = values["total_liabilities_2025"]
reported_equity = values["total_equity_2025"]
reported_assets = values["total_assets_2025"]

print(f"Calculated Liabilities: ${calculated_liabilities:,.2f} million")
print(f"Reported Liabilities: ${reported_liabilities:,.2f} million")

liability_difference = calculated_liabilities - reported_liabilities

print(f"Liability Difference: ${liability_difference:,.2f} million")

assert abs(liability_difference) < 0.01, (
    "2025 detailed liabilities do not reconcile"
)

balance_sheet_difference = (
    reported_assets - calculated_liabilities - reported_equity
)

assert abs(balance_sheet_difference) < 0.01, (
    "2025 assets do not equal liabilities plus equity"
)

print("PASS: 2025 detailed liabilities reconcile")
print("PASS: 2025 assets equal liabilities plus equity")