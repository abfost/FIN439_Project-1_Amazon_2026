"""Amazon connected preliminary forecast and DCF engine.

USD millions; valuation date September 1, 2026.
Simplified financial model; not fully independently validated.
"""

from datetime import date
from typing import Any

import pandas as pd

from financial_model import financial_results
from fixed_assets import fixed_asset_forecast
from working_capital import working_capital

VALUATION_DATE = date(2026, 9, 1)
YEARS = range(2026, 2031)

TAX_RATE = 0.20
DEPRECIATION_RATE = 0.20
NWC_RATIO = -0.14
TERMINAL_REFERENCE_PRICE = 254.92

DEFAULTS = {
    "wacc": 0.1053,
    "terminal_growth": 0.03,
    "operating_margin_change": 0.0,
    "capex_rate_change": 0.0,
}

data = pd.read_csv("Data/amazon_inputs.csv")
values = dict(zip(data["metric"], data["value"]))

REVENUE = {
    year: financial_results[year]["revenue"]
    for year in YEARS
}

BASE_FCFF = {}

for year in YEARS:
    ebit = financial_results[year]["operating_income"]
    depreciation = fixed_asset_forecast[year]["depreciation"]
    capex = fixed_asset_forecast[year]["capex"]

    previous_nwc = (
        working_capital[2025]
        if year == 2026
        else REVENUE[year - 1] * NWC_RATIO
    )
    change_nwc = REVENUE[year] * NWC_RATIO - previous_nwc

    BASE_FCFF[year] = (
        ebit * (1 - TAX_RATE)
        + depreciation
        - capex
        - change_nwc
    )


def run_analysis(inputs: dict[str, Any]) -> dict[str, Any]:
    assumptions = DEFAULTS | inputs

    wacc = float(assumptions["wacc"])
    growth = float(assumptions["terminal_growth"])
    margin_change = float(assumptions["operating_margin_change"])
    capex_change = float(assumptions["capex_rate_change"])

    if not 0.07 <= wacc <= 0.15:
        raise ValueError("WACC outside permitted range")
    if not 0.01 <= growth <= 0.05 or growth >= wacc:
        raise ValueError("Invalid terminal growth rate")
    if not -0.03 <= margin_change <= 0.03:
        raise ValueError("Invalid operating margin change")
    if not -0.05 <= capex_change <= 0.05:
        raise ValueError("Invalid CapEx change")

    cash = float(values["cash_and_equivalents_2025"])
    equity = float(values["total_equity_2025"])
    beginning_ppe = float(values["net_property_equipment_2025"])
    previous_nwc = working_capital[2025]

    # Hold other assets and nonoperating liabilities constant.
    # These are simplifying assumptions, not forecasts.
    operating_assets_2025 = (
        values["inventory_2025"]
        + values["receivables_other_2025"]
    )
    operating_liabilities_2025 = (
        values["accounts_payable_2025"]
        + values["accrued_expenses_other_2025"]
        + values["unearned_revenue_2025"]
    )

    other_assets = (
        values["total_assets_2025"]
        - values["cash_and_equivalents_2025"]
        - values["net_property_equipment_2025"]
        - operating_assets_2025
    )
    other_liabilities = (
        values["total_liabilities_2025"]
        - operating_liabilities_2025
    )

    income_statement = {}
    cash_flow_statement = {}
    balance_sheet = {}
    forecast = {}
    pv_explicit = 0.0

    for year in YEARS:
        revenue = REVENUE[year]

        # Income statement.
        ebit = (
            financial_results[year]["operating_income"]
            + revenue * margin_change
        )
        pretax_income = ebit  # Nonoperating income set to zero.
        tax_expense = max(pretax_income, 0) * TAX_RATE
        net_income = pretax_income - tax_expense

        # Fixed assets and depreciation.
        depreciation = beginning_ppe * DEPRECIATION_RATE
        base_capex = fixed_asset_forecast[year]["capex"]
        capex = base_capex + revenue * capex_change
        ending_ppe = beginning_ppe + capex - depreciation

        # Working capital.
        nwc = revenue * NWC_RATIO
        change_nwc = nwc - previous_nwc

        # Indirect cash flow statement.
        operating_cash_flow = (
            net_income + depreciation - change_nwc
        )
        investing_cash_flow = -capex
        financing_cash_flow = 0.0
        beginning_cash = cash
        cash = (
            beginning_cash + operating_cash_flow
            + investing_cash_flow + financing_cash_flow
        )

        # Equity roll-forward: assumes all earnings retained.
        equity += net_income

        # Aggregate balance-sheet diagnostic.
        net_operating_assets = cash + nwc + ending_ppe + other_assets
        other_liabilities_and_equity = other_liabilities + equity
        bs_difference = (
            net_operating_assets - other_liabilities_and_equity
        )

        # FCFF valuation.
        after_tax_ebit = ebit * (1 - TAX_RATE)
        fcff = (
            after_tax_ebit + depreciation - capex - change_nwc
        )

        remaining_fcff = fcff * (4 / 12) if year == 2026 else fcff
        t = (date(year, 12, 31) - VALUATION_DATE).days / 365.25
        pv_fcff = remaining_fcff / (1 + wacc) ** t
        pv_explicit += pv_fcff

        income_statement[year] = {
            "revenue": revenue,
            "operating_income": ebit,
            "pretax_income": pretax_income,
            "tax_expense": tax_expense,
            "net_income": net_income,
        }

        cash_flow_statement[year] = {
            "net_income": net_income,
            "depreciation": depreciation,
            "change_nwc": change_nwc,
            "operating_cash_flow": operating_cash_flow,
            "capex": capex,
            "investing_cash_flow": investing_cash_flow,
            "financing_cash_flow": financing_cash_flow,
            "ending_cash": cash,
        }

        balance_sheet[year] = {
            "beginning_cash": beginning_cash,
            "ending_cash": cash,
            "operating_nwc": nwc,
            "net_ppe": ending_ppe,
            "equity": equity,
            "aggregate_bs_difference": bs_difference,
        }

        forecast[year] = {
            "revenue": revenue,
            "fcff": fcff,
            "discounted_fcff": pv_fcff,
        }

        previous_nwc = nwc
        beginning_ppe = ending_ppe

    terminal_fcff = forecast[2030]["fcff"]
    terminal_value = (
        terminal_fcff * (1 + growth) / (wacc - growth)
    )
    terminal_years = (
        date(2030, 12, 31) - VALUATION_DATE
    ).days / 365.25
    pv_terminal = terminal_value / (1 + wacc) ** terminal_years

    enterprise_value = pv_explicit + pv_terminal

    # June 2026 valuation bridge, still provisional.
    debt = float(values["long_term_debt_carrying_2026_q2"])
    cash_for_valuation = float(
        values["cash_and_equivalents_2026_q2"]
    )
    securities = float(
        values["marketable_securities_2026_q2"]
    )
    shares = float(values["shares_outstanding_2026_q2"])

    equity_value = (
        enterprise_value - debt + cash_for_valuation + securities
    )
    value_per_share = equity_value / shares

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "upside_downside": (
            value_per_share / TERMINAL_REFERENCE_PRICE - 1
        ),
        "reference_price": TERMINAL_REFERENCE_PRICE,
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
        "forecast": forecast,
        "income_statement": income_statement,
        "cash_flow_statement": cash_flow_statement,
        "balance_sheet": balance_sheet,
        "assumptions": assumptions,
    }


if __name__ == "__main__":
    base = run_analysis({})
    higher_margin = run_analysis({
        "operating_margin_change": 0.01
    })
    higher_capex = run_analysis({
        "capex_rate_change": 0.01
    })

    assert (
        higher_margin["value_per_share"]
        > base["value_per_share"]
    )
    assert (
        higher_capex["value_per_share"]
        < base["value_per_share"]
    )
    for row in base["balance_sheet"].values():
        assert abs(row["aggregate_bs_difference"]) < 0.01

    print(f"Base share price: ${base['value_per_share']:.2f}")
    print("PASS: Connected preliminary forecast and DCF checks")
