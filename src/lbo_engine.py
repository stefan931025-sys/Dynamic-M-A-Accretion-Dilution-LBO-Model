class LBOEngine:
    def __init__(
        self,
        entry_enterprise_value: float,
        initial_debt: float,
        sponsor_equity_pct: float,
        annual_free_cash_flow: float,
        exit_multiple: float,
        exit_ebitda: float,
        holding_period_years: int
    ):
        self.entry_enterprise_value = entry_enterprise_value
        self.initial_debt = initial_debt
        self.sponsor_equity_pct = sponsor_equity_pct
        self.annual_free_cash_flow = annual_free_cash_flow
        self.exit_multiple = exit_multiple
        self.exit_ebitda = exit_ebitda
        self.holding_period_years = holding_period_years
        
        # Calculate sponsor equity investment based on entry valuation and equity percentage
        self.equity = self.entry_enterprise_value * self.sponsor_equity_pct

    def run_debt_schedule(self, holding_period_years: int = None, annual_ebitda_growth: float = 0.08) -> dict:
        """Simulates annual cash flows and debt paydown over the holding period."""
        hp = holding_period_years if holding_period_years is not None else self.holding_period_years
        current_debt = self.initial_debt
        fcf_list = [self.annual_free_cash_flow] * hp

        for fcf in fcf_list:
            current_debt = max(0.0, current_debt - fcf)

        return {
            "Ending_Debt": current_debt,
            "Free_Cash_Flows": fcf_list
        }

    def calculate_returns(self, exit_multiple: float = None, holding_period_years: int = None) -> dict:
        """Calculates exit enterprise/equity values, MOIC, and IRR for the LBO transaction."""
        em = exit_multiple if exit_multiple is not None else self.exit_multiple
        hp = holding_period_years if holding_period_years is not None else self.holding_period_years
        
        projection = self.run_debt_schedule(holding_period_years=hp)
        exit_enterprise_value = self.exit_ebitda * em
        exit_equity_value = exit_enterprise_value - projection["Ending_Debt"]

        moic = exit_equity_value / self.equity if self.equity > 0 else 0.0
        irr = (moic ** (1 / hp)) - 1 if moic > 0 else 0.0

        return {
            "Exit_Enterprise_Value": exit_enterprise_value,
            "Exit_Equity_Value": exit_equity_value,
            "MOIC": moic,
            "IRR": irr
        }
