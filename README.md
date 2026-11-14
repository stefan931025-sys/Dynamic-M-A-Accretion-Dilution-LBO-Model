# Quantitative M&A Accretion/Dilution & LBO Valuation Engine

![Build Status](https://github.com/stefan931025-sys/DCF-Valuation-Model/actions/workflows/ci.yml/badge.svg) ![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A quantitative corporate finance and valuation engine built in Python to evaluate buy-side acquisition scenarios, model pro-forma EPS accretion/dilution under dynamic capital structures, and simulate LBO debt waterfall returns across vectorized sensitivity matrices.

---

## 🚀 Core Capabilities

* **Pro-Forma EPS Accretion/Dilution Modeling:** Dynamically calculates post-transaction net income adjustments, goodwill creation, debt interest expense after tax shields, and new share issuance based on cash vs. stock consideration mix.
* **LBO Debt Waterfall & Returns Engine:** Simulates Senior, Mezzanine, and Equity tranches, tracking mandatory debt amortization, cash flow sweeps, IRR (Internal Rate of Return), and MoIC (Multiple on Invested Capital) across variable holding horizons.
* **Vectorized Sensitivity Engine:** Generates multi-variable matrices using NumPy/Pandas to stress-test transaction viability across purchase multiples, cost synergy execution rates, and exit valuation ranges.
* **Synergy & Goodwill Accounting Integration:** Handles pre-tax cost and revenue synergies, transaction fees amortization, tax asset write-ups, and balance sheet pro-forma adjustments.

---

## 📐 Mathematical Specification & Valuation Mechanics

### 1. Pro-Forma EPS Accretion / Dilution Formula

$$\text{Pro-Forma EPS} = \frac{\text{Acquirer Net Income} + \text{Target Net Income} + \text{After-Tax Synergies} - \text{After-Tax Interest Expense}}{\text{Acquirer Shares Outstanding} + \text{New Shares Issued}}$$

* **After-Tax Interest Expense** = $(\text{New Debt Raised} \times r_{\text{debt}}) \times (1 - \tau)$
* **New Shares Issued** = $\frac{\text{Purchase Price} - \text{Cash Consideration}}{\text{Acquirer Share Price}}$

### 2. Leveraged Buyout (LBO) IRR & Capital Waterfall

$$\text{MoIC} = \frac{\text{Exit Equity Value}}{\text{Sponsor Initial Equity Invested}}$$

$$\text{Sponsor IRR} = (\text{MoIC})^{\frac{1}{t}} - 1$$

---

## 🛠️ System Architecture & Data Flow

* **`src/lbo_ma_engine.py`:** Core computational engine containing dataclasses for parameter encapsulation and static methods for vectorized valuation loops.
* **`tests/`:** Automated unit test suite verifying numerical stability, edge cases, and temporal integrity.
* **CI/CD Pipeline:** GitHub Actions integration running continuous AST auditing (`repo_auditor.py`), static analysis (`flake8`, `bandit`, `mypy`), and rigorous `pytest` validation.

---

## 📐 Methodology, Assumptions & Limitations

### Core Modeling Assumptions
* **Stationarity & Regime Consistency:** Assumes target financial performance and synergy realization rates remain stable within forecast windows.
* **Frictionless Execution:** Baseline evaluations assume deterministic deal execution without unforeseen regulatory penalties or financing friction.

### Known Edge Cases & Failure Modes
* **Synergy Underperformance Risk:** Valuations degrade rapidly if projected cost/revenue synergies fail to materialize post-close, resulting in immediate EPS dilution.
* **Leverage Sensitivity:** High debt-to-EBITDA ratios increase default vulnerability during macroeconomic downturns or rising interest rate shocks.

### Proposed Architectural Extensions
* **Monte Carlo Exit Valuations:** Incorporate stochastic exit multiples driven by historical industry volatility to establish probabilistic return distributions.
* **Dynamic Debt Paydown Modeling:** Expand the LBO engine to handle dynamic cash flow sweeps against multiple senior tranches simultaneously.
