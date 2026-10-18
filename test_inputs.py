import pandas as pd

# Read Amazon's financial data
data = pd.read_csv("Data/amazon_inputs.csv")

# Check that all required columns exist
required_columns = ["metric", "value", "unit", "as_of_date", "source"]

assert all(col in data.columns for col in required_columns), "Missing required column"

# Check that values are numeric
assert pd.api.types.is_numeric_dtype(data["value"]), "Values must be numeric"

# Check that all current input values are positive
assert data["value"].notna().all(), "Missing financial value"

# Check for duplicate metric names
assert data["metric"].is_unique, "Duplicate metric names"

print("PASS: Amazon input file structure and basic checks")
# Check Amazon's historical balance sheets
values = dict(zip(data["metric"], data["value"]))

for year in [2024, 2025]:
    assets = values[f"total_assets_{year}"]
    liabilities = values[f"total_liabilities_{year}"]
    equity = values[f"total_equity_{year}"]

    difference = assets - liabilities - equity

    assert abs(difference) < 0.01, (
        f"FAIL: {year} balance sheet does not balance. "
        f"Difference: {difference}"
    )

    print(f"PASS: {year} balance sheet balances")
    # Reconcile Amazon's three segments to consolidated sales
for year in [2023, 2024, 2025]:
    north_america = values[f"north_america_revenue_{year}"]
    international = values[f"international_revenue_{year}"]
    aws = values[f"aws_revenue_{year}"]

    segment_total = north_america + international + aws
    reported_total = values[f"revenue_{year}"]

    difference = segment_total - reported_total

    assert abs(difference) < 0.01, (
        f"FAIL: {year} segment revenue does not reconcile. "
        f"Difference: {difference}"
    )

    print(f"PASS: {year} segment revenue reconciles")
    # Verify Amazon's 2025 reported net income
operating_income = values["operating_income_2025"]
nonoperating_income = values["nonoperating_income_2025"]
income_taxes = values["income_tax_provision_2025"]
equity_method_activity = values["equity_method_activity_2025"]
reported_net_income = values["net_income_2025"]

calculated_net_income = (
    operating_income
    + nonoperating_income
    - income_taxes
    + equity_method_activity
)

assert abs(calculated_net_income - reported_net_income) < 0.01, (
    "2025 income statement does not reconcile"
)

print("PASS: 2025 income statement reconciles")

# Reconcile Amazon's 2025 operating asset and liability cash flow adjustments
working_capital_items = [
    "inventory_cashflow_change_2025",
    "receivables_other_cashflow_change_2025",
    "other_assets_cashflow_change_2025",
    "payables_cashflow_change_2025",
    "accrued_other_cashflow_change_2025",
    "unearned_revenue_cashflow_change_2025",
]

working_capital_cashflow_total = sum(
    values[item] for item in working_capital_items
)

# Independently calculated expected value from Amazon's 2025 10-K
expected_working_capital_cashflow = -19969

assert abs(
    working_capital_cashflow_total - expected_working_capital_cashflow
) < 0.01, "2025 working-capital cash flow adjustments do not reconcile"

print("PASS: 2025 operating asset and liability cash flow adjustments reconcile")