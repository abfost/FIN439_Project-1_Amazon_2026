
"""FIN 43900 Week 3 published DCF training-case reconciliation.

This is a standalone DCF calculator using the published training
inputs, not a test of Amazon's complete connected forecast engine.
All dollar amounts are USD millions except per-share values.
"""


def calculate_dcf(starting_fcff, growth_rates, wacc,
                  terminal_growth, cash, debt, shares):
    fcff = starting_fcff
    present_value = 0.0
    annual_results = []

    for year, growth in enumerate(growth_rates, start=1):
        fcff = fcff * (1 + growth)
        discounted = fcff / (1 + wacc) ** year
        present_value += discounted
        annual_results.append((year, fcff, discounted))

    if wacc <= terminal_growth:
        raise ValueError("WACC must exceed terminal growth")

    terminal_value = (
        fcff * (1 + terminal_growth)
        / (wacc - terminal_growth)
    )
    pv_terminal = terminal_value / (1 + wacc) ** len(growth_rates)

    enterprise_value = present_value + pv_terminal
    equity_value = enterprise_value + cash - debt
    value_per_share = equity_value / shares

    return {
        "annual_results": annual_results,
        "terminal_value": terminal_value,
        "enterprise_value": enterprise_value,
        "value_per_share": value_per_share,
    }


inputs = {
    "starting_fcff": 100.0,
    "growth_rates": [0.08, 0.06, 0.05, 0.04, 0.03],
    "wacc": 0.10,
    "terminal_growth": 0.03,
    "cash": 50.0,
    "debt": 300.0,
    "shares": 50.0,
}

base = calculate_dcf(**inputs)

print("FIN 43900 OFFICIAL TRAINING CASE")
for year, fcff, discounted in base["annual_results"]:
    print(
        f"Year {year}: FCFF = ${fcff:,.2f}M; "
        f"PV = ${discounted:,.2f}M"
    )

print(f"Terminal value: ${base['terminal_value']:,.2f}M")
print(f"Enterprise value: ${base['enterprise_value']:,.2f}M")
print(f"Value per share: ${base['value_per_share']:,.2f}")

# Published Week 3 answer checks, allowing rounding.
expected = {
    "year_1_fcff": 108.00,
    "year_1_pv": 98.18,
    "terminal_value": 1894.65,
    "enterprise_value": 1624.87,
    "value_per_share": 27.50,
}

observed = {
    "year_1_fcff": base["annual_results"][0][1],
    "year_1_pv": base["annual_results"][0][2],
    "terminal_value": base["terminal_value"],
    "enterprise_value": base["enterprise_value"],
    "value_per_share": base["value_per_share"],
}

for key in expected:
    difference = abs(observed[key] - expected[key])
    print(
        f"{key}: difference = {difference:.4f}; "
        f"{'PASS' if difference <= 0.05 else 'FAIL'}"
    )
    assert difference <= 0.05, f"{key} reconciliation failed"

# Directional changed-input check.
higher_wacc = calculate_dcf(
    **{**inputs, "wacc": 0.11}
)

assert (
    higher_wacc["enterprise_value"]
    < base["enterprise_value"]
)

print(
    "PASS: Raising WACC from 10% to 11% "
    "reduces enterprise value"
)
print("PASS: Published training-case checks completed")
