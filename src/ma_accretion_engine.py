"""
M&A Accretion / Dilution Engine
Models pro-forma net income, debt/stock financing mix, synergetic tax shields, 
and post-deal EPS impact.
"""

from typing import Dict


class MAAccretionEngine:
    """Computes buy-side transaction pro-forma accretion/dilution metrics."""

    def __init__(
        self,
        acquirer_net_income: float,
        acquirer_shares: float,
        acquirer_stock_price: float,
        target_net_income: float,
        target_shares: float,
        offer_price_per_share: float,
        debt_financing_pct: float = 0.60,
        debt_interest_rate: float = 0.065,
        after_tax_synergies: float = 10_000_000,
        tax_rate: float = 0.25,
    ):
        self.acquirer_ni = acquirer_net_income
        self.acquirer_shares = acquirer_shares
        self.acquirer_price = acquirer_stock_price
        self.target_ni = target_net_income
        self.target_shares = target_shares
        self.offer_price = offer_price_per_share
        self.debt_pct = debt_financing_pct
        self.equity_pct = 1.0 - debt_financing_pct
        self.interest_rate = debt_interest_rate
        self.synergies = after_tax_synergies
        self.tax_rate = tax_rate

    def evaluate_transaction(self) -> Dict[str, float]:
        """Calculates Standalone vs Pro-Forma EPS and Accretion percentage."""
        standalone_eps = self.acquirer_ni / self.acquirer_shares
        target_equity_purchase_value = self.target_shares * self.offer_price

        debt_raised = target_equity_purchase_value * self.debt_pct
        equity_issued_value = target_equity_purchase_value * self.equity_pct

        # Interest expense on new debt issuance
        pre_tax_interest = debt_raised * self.interest_rate
        after_tax_interest = pre_tax_interest * (1.0 - self.tax_rate)

        # New shares issued for equity portion
        new_shares_issued = equity_issued_value / self.acquirer_price
        pro_forma_shares = self.acquirer_shares + new_shares_issued

        # Pro-forma net income
        pro_forma_ni = (
            self.acquirer_ni
            + self.target_ni
            + self.synergies
            - after_tax_interest
        )

        pro_forma_eps = pro_forma_ni / pro_forma_shares
        accretion_pct = ((pro_forma_eps - standalone_eps) / standalone_eps) * 100.0

        return {
            "Purchase_Equity_Value": round(target_equity_purchase_value, 2),
            "Debt_Financed": round(debt_raised, 2),
            "Equity_Financed": round(equity_issued_value, 2),
            "Standalone_Acquirer_EPS": round(standalone_eps, 2),
            "Pro_Forma_EPS": round(pro_forma_eps, 2),
            "Accretion_Dilution_Pct": round(accretion_pct, 2),
            "Is_Accretive": bool(accretion_pct > 0),
        }
