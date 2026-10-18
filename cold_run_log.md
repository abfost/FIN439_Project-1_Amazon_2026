
# Amazon Project 1 — Local Restart and Test Log

Date: October 17, 2026

## Environment
- Operating system: Windows
- Application: Python / Streamlit
- Project: FIN439_Project 1_Amazon

## Tests performed
- Known-answer FCFF test: PASS
- Five valuation arithmetic tests: PASS
- Preliminary three-statement linkage tests: PASS
- Streamlit dashboard launched successfully on port 8504
- CapEx sensitivity: increasing capital spending reduced estimated value per share
- Base-case reset check: PASS
- Hypothetical terminal-growth validation demonstration: PASS/FAIL messages displayed as expected

## Limitations
This records successful local tests and an application restart, not a fully isolated clean-environment installation. The financial model remains preliminary, and independent source and accounting verification are incomplete.
**Independent SEC source check — October 17, 2026:** Checked 2025 consolidated revenue ($716,924 million), AWS revenue ($128,725 million), operating income ($79,975 million), June 2026 cash ($78,213 million), long-term debt carrying value ($128,894 million), and shares outstanding (10,783 million) against Amazon's SEC Forms 10-K and 10-Q. All six checked entries matched the model input CSV. This verifies selected filing inputs, not the complete valuation.

2025 10-K: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
2026 Q2 10-Q: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm
## Separate-Environment Verification — October 17, 2026

- Created a new Python environment: .venv_coldtest
- Installed dependencies from requirements.txt: PASS
- Ran five valuation arithmetic tests in the new environment: ALL PASS
- Launched the Streamlit dashboard on port 8505: PASS
- Confirmed the dashboard displayed valuation results and responded to an adjustable input: PASS

Limitation: This test used the existing project folder and a new Python environment. It was not an isolated GitHub clone or an independent review of the financial model.