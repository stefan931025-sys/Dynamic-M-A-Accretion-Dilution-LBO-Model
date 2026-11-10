# Quantitative M&A Accretion/Dilution & LBO Valuation Engine

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/stefan931025-sys/Dynamic-M-A-Accretion-Dilution-LBO-Model)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A quantitative corporate finance and valuation engine built in Python to evaluate buy-side acquisition scenarios, model pro-forma EPS accretion/dilution under dynamic capital structures, and simulate LBO debt waterfall returns across vectorized sensitivity matrices.

---

## Core Capabilities

* **Pro-Forma EPS Accretion/Dilution Modeling:** Dynamically calculates post-transaction net income adjustments, goodwill creation, debt interest expense after tax shields, and new share issuance based on cash vs. stock consideration mix.
* **LBO Debt Waterfall & Returns Engine:** Simulates Senior, Mezzanine, and Equity tranches, tracking mandatory debt amortization, cash flow sweeps, IRR (Internal Rate of Return), and MoIC (Multiple on Invested Capital) across variable holding horizons.
* **Vectorized Sensitivity Engine:** Generates multi-variable matrices using NumPy/Pandas to stress-test transaction viability across purchase multiples, cost synergy execution rates, and exit valuation ranges.
* **Synergy & Goodwill Accounting Integration:** Handles pre-tax cost and revenue synergies, transaction fees amortization, tax asset write-ups, and balance sheet pro-forma adjustments.

---

## Mathematical Specification & Valuation Mechanics

### 1. Pro-Forma EPS Accretion / Dilution Formula

$$\text{Pro-Forma EPS} = \frac{\text{Acquirer Net Income} + \text{Target Net Income} + \text{After-Tax Synergies} - \text{After-Tax Interest Expense}}{\text{Acquirer Shares Outstanding} + \text{New Shares Issued}}$$

Where:
$$\text{After-Tax Interest Expense} = (\text{New Debt Raised} \times r_{\text{debt}}) \times (1 - \tau)$$
$$\text{New Shares Issued} = \frac{\text{Purchase Price} \times \% \text{Stock Consideration}}{\text{Acquirer Share Price}}$$

### 2. Leveraged Buyout (LBO) IRR & Capital Waterfall

$$\text{MoIC} = \frac{\text{Exit Equity Value}}{\text{Sponsor Initial Equity Invested}}$$

$$\text{Sponsor IRR} = \left( \text{MoIC} \right)^{\frac{1}{t}} - 1$$

---

## System Architecture & Data Flow

