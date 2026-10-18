# Amazon preliminary WACC calculation
# Valuation date: September 1, 2026
# All financial values in USD millions

risk_free_rate = 0.0479
equity_risk_premium = 0.0414
beta = 1.46

# Provisional assumptions
pretax_cost_of_debt = 0.05
marginal_tax_rate = 0.21

# Market value of equity
share_price = 254.92
shares_outstanding_millions = 10786.314
market_equity = share_price * shares_outstanding_millions

# Debt carrying-value proxy
debt_value = 128894

# Cost of equity using CAPM
cost_of_equity = risk_free_rate + beta * equity_risk_premium

# Capital structure weights
total_capital = market_equity + debt_value
equity_weight = market_equity / total_capital
debt_weight = debt_value / total_capital

# Weighted average cost of capital
wacc = (
    equity_weight * cost_of_equity
    + debt_weight * pretax_cost_of_debt * (1 - marginal_tax_rate)
)

print("\nAMAZON PRELIMINARY WACC CALCULATION")
print(f"Market Value of Equity: ${market_equity:,.2f} million")
print(f"Debt Value Proxy: ${debt_value:,.2f} million")
print(f"Cost of Equity: {cost_of_equity:.2%}")
print(f"Pretax Cost of Debt: {pretax_cost_of_debt:.2%}")
print(f"Equity Weight: {equity_weight:.2%}")
print(f"Debt Weight: {debt_weight:.2%}")
print(f"Marginal Tax Rate: {marginal_tax_rate:.2%}")
print(f"Preliminary WACC: {wacc:.2%}")

assert abs(equity_weight + debt_weight - 1.0) < 1e-10
assert 0 < wacc < 1

print("\nPASS: Preliminary WACC calculation completed")