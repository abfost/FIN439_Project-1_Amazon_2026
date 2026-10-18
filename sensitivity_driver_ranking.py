
"""Amazon one-at-a-time sensitivity and driver ranking.

Uses the connected preliminary model in analysis.py.
All operating income and FCFF amounts are USD millions.
"""

import csv
from pathlib import Path

from analysis import DEFAULTS, run_analysis


BASE = run_analysis({})

# Changes are in decimal units: 0.01 = one percentage point.
DRIVERS = {
    "WACC": ("wacc", 0.005, 0.01),
    "Terminal growth": ("terminal_growth", 0.005, 0.01),
    "Operating margin": ("operating_margin_change", 0.005, 0.01),
    "CapEx/revenue": ("capex_rate_change", 0.005, 0.01),
}

rows = []

for label, (key, narrow, wide) in DRIVERS.items():
    for range_name, step in [
        ("Narrow", narrow),
        ("Wide", wide),
    ]:
        base_input = DEFAULTS[key]

        low = run_analysis({
            key: base_input - step
        })

        high = run_analysis({
            key: base_input + step
        })

        low_ebit = low["income_statement"][2030]["operating_income"]
        high_ebit = high["income_statement"][2030]["operating_income"]

        low_fcff = low["forecast"][2030]["fcff"]
        high_fcff = high["forecast"][2030]["fcff"]

        low_value = low["value_per_share"]
        high_value = high["value_per_share"]

        rows.append({
            "driver": label,
            "range": range_name,
            "low_input": base_input - step,
            "high_input": base_input + step,
            "2030_ebit_swing_millions": round(
                abs(high_ebit - low_ebit), 2
            ),
            "2030_fcff_swing_millions": round(
                abs(high_fcff - low_fcff), 2
            ),
            "valuation_swing_per_share": round(
                abs(high_value - low_value), 2
            ),
            "value_per_share_low_input": round(low_value, 2),
            "value_per_share_high_input": round(high_value, 2),
        })


output = Path("Output")
output.mkdir(exist_ok=True)
path = output / "sensitivity_driver_ranking.csv"

with path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)


print("\nAMAZON DRIVER SENSITIVITY RANKINGS")
print(f"Base equity value/share: ${BASE['value_per_share']:.2f}")

for range_name in ("Narrow", "Wide"):
    print(f"\n{range_name.upper()} RANGE")

    group = [
        row for row in rows
        if row["range"] == range_name
    ]

    for metric in (
        "2030_ebit_swing_millions",
        "2030_fcff_swing_millions",
        "valuation_swing_per_share",
    ):
        ranking = sorted(
            group,
            key=lambda row: row[metric],
            reverse=True,
        )

        print(f"\nRanking by {metric}:")
        for position, row in enumerate(ranking, start=1):
            print(
                f"{position}. {row['driver']}: "
                f"{row[metric]:,.2f}"
            )

print(f"\nResults saved: {path}")
