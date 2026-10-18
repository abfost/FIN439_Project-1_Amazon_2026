"""Tests for Amazon's preliminary three-statement forecast.

These verify internal arithmetic relationships, not the
completeness of the financial model.
"""

from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import forecast_working_capital
from three_statement_model import cash_flow_bridge
from balance_sheet_forecast import balance_sheet_forecast

TOLERANCE = 0.02

for year in range(2026, 2031):
    income = financial_results[year]
    ppe = fixed_asset_forecast[year]
    nwc = forecast_working_capital[year]
    cashflow = cash_flow_bridge[year]
    balance = balance_sheet_forecast[year]

    # 1. Cash flow statement must link to income statement.
    assert abs(
        cashflow["net_income"] - income["net_income"]
    ) < TOLERANCE, f"{year}: Net income does not link"

    # 2. Cash flow D&A must link to PP&E schedule.
    assert abs(
        cashflow["depreciation"] - ppe["depreciation"]
    ) < TOLERANCE, f"{year}: Depreciation mismatch"

    # 3. Cash flow working capital movement must match schedule.
    assert abs(
        cashflow["change_nwc"] - nwc["change_in_nwc"]
    ) < TOLERANCE, f"{year}: NWC mismatch"

    # 4. PP&E must roll forward properly.
    expected_ppe = (
        ppe["beginning_ppe"]
        + ppe["capex"]
        - ppe["depreciation"]
    )

    assert abs(
        ppe["ending_ppe"] - expected_ppe
    ) < TOLERANCE, f"{year}: PP&E does not roll forward"

    # 5. Cash must roll forward using cash flow.
    expected_cash = (
        balance["beginning_cash"]
        + cashflow["operating_cash_flow"]
        - cashflow["capex"]
    )

    assert abs(
        balance["ending_cash"] - expected_cash
    ) < TOLERANCE, f"{year}: Cash does not roll forward"

    # 6. Ending NWC must link to working capital schedule.
    assert abs(
        balance["operating_nwc"] - nwc["operating_nwc"]
    ) < TOLERANCE, f"{year}: NWC balance mismatch"

    print(f"PASS: {year} income, cash flow, PP&E, and NWC links")

print("\nPASS: Preliminary three-statement link tests completed")
print(
    "WARNING: These are internal consistency checks, "
    "not a complete independent balance-sheet validation."
)