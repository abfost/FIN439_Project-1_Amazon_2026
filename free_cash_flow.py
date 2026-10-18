# Amazon preliminary free cash flow forecast
# All amounts are in USD millions

from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import forecast_working_capital

tax_rate = 0.20

fcff_forecast = {}

print("\nAMAZON FIVE-YEAR FREE CASH FLOW FORECAST")
print("All figures in USD millions")

for year in range(2026, 2031):
    operating_income = financial_results[year]["operating_income"]
    depreciation = fixed_asset_forecast[year]["depreciation"]
    capex = fixed_asset_forecast[year]["capex"]
    change_nwc = forecast_working_capital[year]["change_in_nwc"]

    after_tax_operating_income = operating_income * (1 - tax_rate)

    fcff = (
        after_tax_operating_income
        + depreciation
        - capex
        - change_nwc
    )

    fcff_forecast[year] = fcff

    print(f"\n{year}")
    print(f"  After-Tax EBIT: ${after_tax_operating_income:,.2f} million")
    print(f"  Depreciation: ${depreciation:,.2f} million")
    print(f"  Capital Expenditures: ${capex:,.2f} million")
    print(f"  Change in NWC: ${change_nwc:,.2f} million")
    print(f"  FCFF: ${fcff:,.2f} million")

print("\nPASS: Preliminary FCFF forecast calculated")