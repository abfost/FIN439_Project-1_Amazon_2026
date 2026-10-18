# Known-answer test: FCFF formula
# All amounts are USD millions
# Expected answer calculated separately: $600 million

ebit = 1000
tax_rate = 0.20
depreciation = 100
capex = 250
change_nwc = 50

expected_fcff = 600

actual_fcff = (
    ebit * (1 - tax_rate)
    + depreciation
    - capex
    - change_nwc
)

difference = actual_fcff - expected_fcff

print("AMAZON PROJECT 1 — KNOWN-ANSWER FORMULA TEST")
print(f"Expected FCFF: ${expected_fcff:,.2f} million")
print(f"Actual FCFF: ${actual_fcff:,.2f} million")
print(f"Difference: ${difference:,.2f} million")

assert abs(difference) < 0.01

print("PASS: Known-answer FCFF calculation")