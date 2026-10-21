import numpy as np
import pandas as pd

def run_ma_model(
    acquirer_eps: float,
    acquirer_share_price: float,
    target_net_income: float,
    purchase_price: float,
    pct_stock_financed: float,
    pct_debt_financed: float,
    interest_rate: float,
    tax_rate: float,
    synergies: float
):
    """
    Computes pro-forma EPS accretion/dilution for an M&A transaction.
    """
    # 1. Purchase Consideration Breakdown
    total_consideration = purchase_price
    stock_consideration = total_consideration * pct_stock_financed
    debt_consideration = total_consideration * pct_debt_financed
    
    # Shares issued to finance the deal
    new_shares_issued = stock_consideration / acquirer_share_price
    
    # New interest expense from debt financing (after-tax)
    annual_pretax_interest = debt_consideration * interest_rate
    after_tax_interest_expense = annual_pretax_interest * (1 - tax_rate)
    
    # 2. Pro-Forma Net Income Calculation
    # Assume acquirer net income can be derived from EPS * existing shares (let's assume base shares = 100M for scaling)
    base_shares = 100_000_000
    acquirer_net_income = acquirer_eps * base_shares
    
    after_tax_synergies = synergies * (1 - tax_rate)
    
    pro_forma_net_income = (
        acquirer_net_income + 
        target_net_income + 
        after_tax_synergies - 
        after_tax_interest_expense
    )
    
    # 3. Pro-Forma Share Count
    pro_forma_shares = base_shares + new_shares_issued
    
    # 4. Pro-Forma EPS & Accretion/Dilution
    pro_forma_eps = pro_forma_net_income / pro_forma_shares
    eps_change_dollar = pro_forma_eps - acquirer_eps
    eps_change_pct = (eps_change_dollar / acquirer_eps) * 100
    
    results = {
        "New Shares Issued": f"{new_shares_issued:,.0f}",
        "After-Tax Interest Expense ($)": f"${after_tax_interest_expense:,.2f}",
        "Pro-Forma Net Income ($)": f"${pro_forma_net_income:,.2f}",
        "Pro-Forma EPS ($)": f"${pro_forma_eps:.2f}",
        "Accretion / (Dilution) ($)": f"${eps_change_dollar:.2f}",
        "Accretion / (Dilution) (%)": f"{eps_change_pct:.2f}%"
    }
    
    return results

# --- EXAMPLE EXECUTION ---
if __name__ == "__main__":
    print("--- M&A ACCRETION / DILUTION BASE CASE ---")
    metrics = run_ma_model(
        acquirer_eps=4.50,
        acquirer_share_price=75.00,
        target_net_income=80_000_000,
        purchase_price=500_000_000,
        pct_stock_financed=0.40,  # 40% stock
        pct_debt_financed=0.60,   # 60% debt
        interest_rate=0.065,      # 6.5% interest on debt
        tax_rate=0.21,            # 21% corporate tax rate
        synergies=15_000_000      # $15M pre-tax synergies
    }
    
    for k, v in metrics.items():
        print(f"{k}: {v}")
