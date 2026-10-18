# Amazon Five-Year Financial Model
# Forecast period: 2026–2030
# All financial figures are in USD millions

from revenue_forecast import five_year_forecast
from operating_income_forecast import operating_margins

segments = ["north_america", "international", "aws"]
years = range(2026, 2031)

financial_results = {}

print("\nAMAZON FIVE-YEAR FORECAST INCOME STATEMENT")
print("All figures in USD millions")

for year in years:
    total_revenue = 0
    total_operating_income = 0

    for segment in segments:
        revenue = five_year_forecast[year][segment]
        margin = operating_margins[segment][year]

        operating_income = revenue * margin

        total_revenue += revenue
        total_operating_income += operating_income

        # Preliminary income statement assumptions
    tax_rate = 0.20

    # Temporary simplifying assumption:
    # Net nonoperating income and equity-method activity = 0.
    # These will need explicit drivers and documentation.
    nonoperating_income = 0
    equity_method_activity = 0

    income_before_taxes = total_operating_income + nonoperating_income
    income_tax_expense = max(income_before_taxes, 0) * tax_rate
    net_income = (
        income_before_taxes
        - income_tax_expense
        + equity_method_activity
    )

    financial_results[year] = {
        "revenue": total_revenue,
        "operating_income": total_operating_income,
        "operating_margin": total_operating_income / total_revenue,
        "nonoperating_income": nonoperating_income,
        "income_before_taxes": income_before_taxes,
        "income_tax_expense": income_tax_expense,
        "net_income": net_income,
    }

    print(f"\n{year}")
    print(f"  Revenue: ${total_revenue:,.2f} million")
    print(f"  Operating Income: ${total_operating_income:,.2f} million")
    print(f"  Operating Margin: {total_operating_income / total_revenue:.2%}")
    print(f"  Income Before Taxes: ${income_before_taxes:,.2f} million")
    print(f"  Income Tax Expense: ${income_tax_expense:,.2f} million")
    print(f"  Net Income: ${net_income:,.2f} million")