import pandas as pd

# Load the existing peer data
peers = pd.read_csv("Data/peer_valuation_inputs.csv")

# Calculate market capitalization
peers["market_cap_millions"] = (
    peers["share_price"] * peers["shares_outstanding_millions"]
)

# Calculate enterprise value when all inputs exist
peers["enterprise_value_millions"] = (
    peers["market_cap_millions"]
    + peers["debt_millions"]
    - peers["cash_millions"]
)

# Calculate required comparable-company multiples
peers["ev_revenue"] = (
    peers["enterprise_value_millions"] /
    peers["ttm_revenue_millions"]
)

peers["pe_ratio"] = (
    peers["market_cap_millions"] /
    peers["ttm_net_income_millions"]
)

columns = [
    "company",
    "market_cap_millions",
    "enterprise_value_millions",
    "ev_revenue",
    "pe_ratio",
]

print("\nAMAZON PROJECT 1 — COMPARABLE VALUATION")
print(peers[columns].round(2).to_string(index=False))

print("\nMissing required data:")
required = [
    "share_price",
    "shares_outstanding_millions",
    "debt_millions",
    "cash_millions",
    "ttm_revenue_millions",
    "ttm_net_income_millions",
]

for _, peer in peers.iterrows():
    missing = [field for field in required if pd.isna(peer[field])]
    print(f"{peer['ticker']}: {', '.join(missing) if missing else 'None'}")

peers.to_csv("Data/peer_valuation_results.csv", index=False)

print("\nResults saved to Data/peer_valuation_results.csv")