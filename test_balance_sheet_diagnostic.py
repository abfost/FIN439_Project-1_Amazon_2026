
"""Test the preliminary aggregate balance-sheet diagnostic.

Recalculates the identity independently of the stored
aggregate_bs_difference field and tests a cash perturbation.
"""

from analysis import run_analysis, values

TOLERANCE = 0.02

result = run_analysis({})

operating_assets_2025 = (
    float(values["inventory_2025"])
    + float(values["receivables_other_2025"])
)

operating_liabilities_2025 = (
    float(values["accounts_payable_2025"])
    + float(values["accrued_expenses_other_2025"])
    + float(values["unearned_revenue_2025"])
)

other_assets = (
    float(values["total_assets_2025"])
    - float(values["cash_and_equivalents_2025"])
    - float(values["net_property_equipment_2025"])
    - operating_assets_2025
)

other_liabilities = (
    float(values["total_liabilities_2025"])
    - operating_liabilities_2025
)


def calculate_difference(balance):
    return (
        balance["ending_cash"]
        + balance["operating_nwc"]
        + balance["net_ppe"]
        + other_assets
        - other_liabilities
        - balance["equity"]
    )


for year, balance in result["balance_sheet"].items():
    recalculated = calculate_difference(balance)

    assert abs(recalculated) < TOLERANCE, (
        f"{year}: Independent aggregate balance-sheet check failed: "
        f"{recalculated:.2f}"
    )

    print(f"PASS: {year} independently recalculated difference = "
          f"{recalculated:.2f} million")


original = result["balance_sheet"][2026]
altered = original.copy()
altered["ending_cash"] += 100

difference = calculate_difference(altered)

assert abs(difference - 100) < TOLERANCE, (
    "FAIL: Cash perturbation was not detected"
)

print(
    "PASS: Deliberate $100 million cash error detected "
    f"(difference = {difference:.2f} million)"
)

print(
    "\nWARNING: This validates an aggregate model identity, "
    "not full account-level financial statements."
)
