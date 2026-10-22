"""
Leveraged Buyout (LBO) & Return Engine
Models sponsor equity check, debt amortization schedule, exit valuation, 
and Internal Rate of Return (IRR) / Multiple on Invested Capital (MoIC).
"""

from typing import Dict


class LBOEngine:
    """Calculates private equity LBO returns and debt paydown."""

    def __init__(
        self,
        entry_enterprise_value: float,
        initial_debt: float,
        sponsor_equity_pct: float,
        annual_free_cash_flow: float,
        exit_multiple: float,
        exit_ebitda: float,
        holding_period_years: int = 5,
    ):
        self.entry_ev = entry_enterprise_value
        self.initial_debt = initial_debt
        self.sponsor_equity = entry_enterprise_value * sponsor_equity_pct
        self.fcf = annual_free_cash_flow
        self.exit_multiple = exit_multiple
        self.exit_ebitda = exit_ebitda
        self.years = holding_period_years

    def run_lbo_model(self) -> Dict[str, float]:
        """Calculates exit equity value, MoIC, and IRR."""
        # Simple debt paydown model using annual FCF
        remaining_debt = max(0.0, self.initial_debt - (self.fcf * self.years))

        # Exit calculations
        exit_ev = self.exit_ebitda * self.exit_multiple
        exit_equity_value = max(0.0, exit_ev - remaining_debt)

        # Returns metrics
        moic = exit_equity_value / self.sponsor_equity
        irr = (moic ** (1.0 / self.years)) - 1.0

        return {
            "Sponsor_Initial_Equity": round(self.sponsor_equity, 2),
            "Remaining_Debt_at_Exit": round(remaining_debt, 2),
            "Exit_Enterprise_Value": round(exit_ev, 2),
            "Exit_Equity_Value": round(exit_equity_value, 2),
            "MoIC": round(moic, 2),
            "IRR_Pct": round(irr * 100.0, 2),
        }
