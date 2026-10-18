# Amazon preliminary September 1, 2026 equity valuation
# Financial values in USD millions
# Not a final or fully reconciled valuation

import pandas as pd

from valuation_date_adjustment import adjusted_enterprise_value
from wacc import share_price

data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

# Latest reported balance sheet available before valuation date
cash = values["cash_and_equivalents_2026_q2"]
marketable_securities = values["marketable_securities_2026_q2"]
debt = values["long_term_debt_carrying_2026_q2"]

# June 30 reported common shares outstanding
shares = values["shares_outstanding_2026_q2"]

# Preliminary EV-to-equity bridge
# Marketable securities included provisionally as nonoperating assets
# Finance leases and other financing claims still require review
equity_value = (
    adjusted_enterprise_value
    - debt
    + cash
    + marketable_securities
)

value_per_share = equity_value / shares
upside_downside = value_per_share / share_price - 1

print("\nAMAZON UPDATED PRELIMINARY EQUITY VALUATION")
print("All financial amounts in USD millions")

print(f"Adjusted Enterprise Value: ${adjusted_enterprise_value:,.2f}")
print(f"Less Debt Carrying Value: ${debt:,.2f}")
print(f"Add Cash: ${cash:,.2f}")
print(f"Add Marketable Securities: ${marketable_securities:,.2f}")
print(f"Preliminary Equity Value: ${equity_value:,.2f}")
print(f"Common Shares Outstanding: {shares:,.2f} million")
print(f"Preliminary Value Per Share: ${value_per_share:,.2f}")
print(f"Reference Market Price: ${share_price:,.2f}")
print(f"Illustrative Upside/Downside: {upside_downside:.2%}")

assert equity_value > 0
assert shares > 0

print("\nPASS: Updated preliminary equity bridge calculated")
print("WARNING: Dilution, lease claims, and timing still require validation.")