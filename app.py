"""Interactive Amazon valuation dashboard for FIN 43900."""

import pandas as pd
import streamlit as st

from analysis import run_analysis, DEFAULTS

st.set_page_config(
    page_title="Amazon Valuation | FIN 43900",
    layout="wide",
)

st.title("Amazon | Investment Valuation")
st.caption(
    "FIN 43900 • Preliminary valuation • "
    "September 1, 2026"
)

st.warning(
    "Preliminary valuation: 2026 stub cash flow, dilution, "
    "leases, capital spending, and other assumptions "
    "still require final validation."
)

# Start with the base-case assumptions.
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_assumptions():
    """Restore the four assumptions to the base case."""
    for key, value in DEFAULTS.items():
        st.session_state[key] = value


with st.sidebar:
    st.header("Valuation assumptions")

    # Display percentages as 10.5%, not 0.1%.
    # Convert percentage points back to decimals for analysis.py.
    wacc_percent = st.slider(
        "WACC (%)",
        min_value=7.0,
        max_value=15.0,
        value=round(st.session_state["wacc"] * 100, 1),
        step=0.1,
        format="%.1f%%",
    )
    st.session_state["wacc"] = wacc_percent / 100

    growth_percent = st.slider(
        "Terminal growth rate (%)",
        min_value=1.0,
        max_value=5.0,
        value=round(st.session_state["terminal_growth"] * 100, 1),
        step=0.1,
        format="%.1f%%",
    )
    st.session_state["terminal_growth"] = growth_percent / 100

    st.slider(
        "Operating margin change (percentage points)",
        min_value=-0.03,
        max_value=0.03,
        step=0.005,
        format="%.3f",
        key="operating_margin_change",
        help="0.010 adds one percentage point to operating margin.",
    )

    st.slider(
        "CapEx / revenue change (percentage points)",
        min_value=-0.05,
        max_value=0.05,
        step=0.005,
        format="%.3f",
        key="capex_rate_change",
        help="0.010 increases CapEx by one percentage point of revenue.",
    )

    st.button(
        "Reset to base case",
        on_click=reset_assumptions,
        width="stretch",
    )

inputs = {
    key: st.session_state[key]
    for key in DEFAULTS
}

# Recalculate whenever the user changes a control.
try:
    result = run_analysis(inputs)
    base = run_analysis({})
except ValueError as error:
    st.error(f"Invalid valuation assumption: {error}")
    st.stop()

st.subheader("Interactive valuation results")

a, b, c = st.columns(3)

a.metric(
    "Estimated value per share",
    f"${result['value_per_share']:,.2f}",
)

b.metric(
    "Reference market price",
    f"${result['reference_price']:,.2f}",
)

c.metric(
    "Upside / downside",
    f"{result['upside_downside']:.1%}",
)

st.metric(
    "Estimated enterprise value",
    f"${result['enterprise_value'] / 1000:,.1f} billion",
)

st.subheader("Base-case comparison")

comparison = pd.DataFrame(
    {
        "Case": ["Base", "Current settings"],
        "Value per share": [
            base["value_per_share"],
            result["value_per_share"],
        ],
    }
).set_index("Case")

st.bar_chart(comparison)

st.subheader("2026–2030 forecast cash flows")

forecast_table = pd.DataFrame.from_dict(
    result["forecast"],
    orient="index",
)

forecast_table.index.name = "Year"

st.dataframe(
    forecast_table.rename(
        columns={
            "revenue": "Revenue ($M)",
            "fcff": "Full-year FCFF ($M)",
            "discounted_fcff": "PV of remaining FCFF ($M)",
        }
    ).round(2),
    width="stretch",
)

st.subheader("Valuation checks")

# Validation demonstration using a deliberately invalid test assumption.
# This does not change the actual valuation inputs or calculated results.

st.markdown("#### Model validation demonstration")

run_invalid_test = st.checkbox(
    "Demonstrate invalid terminal growth assumption",
    value=False,
    help="Tests a hypothetical case where terminal growth equals WACC.",
)

validation_wacc = inputs["wacc"]
validation_growth = (
    validation_wacc
    if run_invalid_test
    else inputs["terminal_growth"]
)

if validation_growth >= validation_wacc:
    st.error(
        "FAIL — Terminal growth must be below WACC. "
        "The perpetuity-growth valuation would be invalid."
    )
else:
    st.success(
        "PASS — Terminal growth is below WACC."
    )

if result["enterprise_value"] > 0:
    terminal_share = (
        result["pv_terminal"] / result["enterprise_value"]
    )
    st.write(
        "Terminal value share of enterprise value:",
        f"{terminal_share:.1%}",
    )
else:
    st.write(
        "Terminal value share of enterprise value: "
        "Not meaningful"
    )

is_base_case = all(
    abs(inputs[key] - DEFAULTS[key]) < (
        0.0005 if key == "wacc" else 1e-8
    )
    for key in DEFAULTS
)

st.write(
    "Reset check:",
    "Base settings restored"
    if is_base_case
    else "Modified assumptions active",
)

st.info(
    "Changing assumptions recalculates FCFF and enterprise value. "
    "This is a preliminary valuation tool, not yet a fully integrated "
    "three-statement forecasting system or independently validated "
    "investment recommendation."
)

# Preliminary financial statement schedules
# These display the baseline forecasts, not recalculated
# financial statements for modified slider assumptions.


st.divider()
st.header("Five-Year Financial Statement Forecasts")

st.caption(
    "Connected preliminary financial statements, 2026–2030. "
    "Operating-margin and CapEx changes flow through the "
    "income statement, cash flow, PP&E, cash, equity, and DCF. "
    "Other important assumptions remain fixed."
)


tab1, tab2, tab3 = st.tabs(
    ["Income Statement", "Cash Flow Statement", "Balance Sheet"]
)

with tab1:
    income_table = pd.DataFrame.from_dict(
        result["income_statement"], orient="index"
    )
    income_table.index.name = "Year"
    st.dataframe(income_table.round(2), width="stretch")

with tab2:
    cash_flow_table = pd.DataFrame.from_dict(
        result["cash_flow_statement"], orient="index"
    )
    cash_flow_table.index.name = "Year"
    st.dataframe(cash_flow_table.round(2), width="stretch")

with tab3:
    balance_table = pd.DataFrame.from_dict(
        result["balance_sheet"], orient="index"
    )
    balance_table.index.name = "Year"
    st.dataframe(balance_table.round(2), width="stretch")

st.warning(
    "These statements remain preliminary. "
    "The balance sheet is not a complete account-level forecast; "
    "noncash adjustments and financing flows remain incomplete."
)