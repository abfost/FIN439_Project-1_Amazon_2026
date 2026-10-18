# Amazon preliminary balance sheet forecast
# All amounts in USD millions

import pandas as pd

from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import forecast_working_capital

data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Reported 2025 starting balances
beginning_cash = values["cash_and_equivalents_2025"]
beginning_equity = values["total_equity_2025"]

balance_sheet_forecast = {}

print("\nAMAZON PRELIMINARY BALANCE SHEET FORECAST")
print("All figures in USD millions")

for year in range(2026, 2031):
    net_income = financial_results[year]["net_income"]

    # Operating working capital and property/equipment
    operating_nwc = forecast_working_capital[year]["operating_nwc"]
    ending_ppe = fixed_asset_forecast[year]["ending_ppe"]

    # Illustrative equity roll-forward before distributions,
    # new stock issuance, and other comprehensive income
    ending_equity = beginning_equity + net_income

    balance_sheet_forecast[year] = {
        "operating_nwc": operating_nwc,
        "net_ppe": ending_ppe,
        "equity_before_other_changes": ending_equity,
    }

    print(f"\n{year}")
    print(f"  Operating NWC: ${operating_nwc:,.2f} million")
    print(f"  Net PP&E: ${ending_ppe:,.2f} million")
    print(f"  Equity before other changes: ${ending_equity:,.2f} million")

    beginning_equity = ending_equity

print("\nPASS: Preliminary balance sheet components calculated")
print("NOTE: Complete balance sheet and independent balance checks still required.")
# Preliminary cash roll-forward
# Assumes no additional financing or investing cash flows
# beyond the modeled operating cash flow and CapEx.

from three_statement_model import cash_flow_bridge

cash_balance = values["cash_and_equivalents_2025"]

print("\nAMAZON PRELIMINARY CASH BALANCE FORECAST")
print("All figures in USD millions")

for year in range(2026, 2031):
    beginning_cash = cash_balance

    operating_cash_flow = cash_flow_bridge[year]["operating_cash_flow"]
    capex = cash_flow_bridge[year]["capex"]

    financing_cash_flow = 0
    other_investing_cash_flow = 0

    ending_cash = (
        beginning_cash
        + operating_cash_flow
        - capex
        + financing_cash_flow
        + other_investing_cash_flow
    )

    balance_sheet_forecast[year]["beginning_cash"] = beginning_cash
    balance_sheet_forecast[year]["ending_cash"] = ending_cash

    print(f"\n{year}")
    print(f"  Beginning Cash: ${beginning_cash:,.2f} million")
    print(f"  Operating Cash Flow: ${operating_cash_flow:,.2f} million")
    print(f"  Capital Expenditures: ${capex:,.2f} million")
    print(f"  Ending Cash: ${ending_cash:,.2f} million")

    cash_balance = ending_cash

print("\nPASS: Preliminary cash balances roll forward")

# Diagnose remaining forecast balance sheet components
# This is a diagnostic, not a complete balance sheet.

print("\nAMAZON FORECAST BALANCE SHEET DIAGNOSTIC")
print("All figures in USD millions")

# Historical non-working-capital assets other than cash and PP&E
other_assets_2025 = (
    values["total_assets_2025"]
    - values["cash_and_equivalents_2025"]
    - values["net_property_equipment_2025"]
    - (
        values["inventory_2025"]
        + values["receivables_other_2025"]
    )
)

# Historical operating liabilities included in NWC
operating_liabilities_2025 = (
    values["accounts_payable_2025"]
    + values["accrued_expenses_other_2025"]
    + values["unearned_revenue_2025"]
)

# Historical liabilities outside operating NWC
other_liabilities_2025 = (
    values["total_liabilities_2025"]
    - operating_liabilities_2025
)

for year in range(2026, 2031):
    result = balance_sheet_forecast[year]

    # NWC already nets operating assets against operating liabilities.
    # This is an aggregate balance sheet identity, not a detailed schedule.
    implied_assets_less_operating_liabilities = (
        result["ending_cash"]
        + result["operating_nwc"]
        + result["net_ppe"]
        + other_assets_2025
    )

    liabilities_and_equity = (
        other_liabilities_2025
        + result["equity_before_other_changes"]
    )

    difference = (
        implied_assets_less_operating_liabilities
        - liabilities_and_equity
    )

    print(f"\n{year}")
    print(f"  Aggregate Asset Side: ${implied_assets_less_operating_liabilities:,.2f}")
    print(f"  Other Liabilities + Equity: ${liabilities_and_equity:,.2f}")
    print(f"  Unreconciled Difference: ${difference:,.2f}")

print("\nNOTE: Differences require accounting investigation, not a plug.")