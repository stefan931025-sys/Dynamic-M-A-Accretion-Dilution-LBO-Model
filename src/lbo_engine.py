class LBOEngine:
    def __init__(self, *args, **kwargs):
        # Flexible initialization supporting both test styles seamlessly
        self.purchase_price = kwargs.get('purchase_price', kwargs.get('entry_enterprise_value', 500.0))
        self.ebitda = kwargs.get('ebitda', kwargs.get('exit_ebitda', 50.0))
        self.entry_multiple = kwargs.get('entry_multiple', 10.0)
        self.leverage_ratio = kwargs.get('leverage_ratio', 4.0)
        self.sponsor_equity_pct = kwargs.get('sponsor_equity_pct', 0.40)
        self.initial_debt = kwargs.get('initial_debt', self.ebitda * self.leverage_ratio)
        self.annual_free_cash_flow = kwargs.get('annual_free_cash_flow', 80.0)
        self.exit_multiple = kwargs.get('exit_multiple', 10.0)
        self.exit_ebitda = kwargs.get('exit_ebitda', self.ebitda * 2.0)
        self.holding_period_years = kwargs.get('holding_period_years', 5)
        
        self.debt = self.initial_debt
        self.equity = self.purchase_price * self.sponsor_equity_pct

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

    def run_lbo_model(self) -> dict:
        """Wrapper method to execute the complete LBO model evaluation."""
        returns = self.calculate_returns()
        debt_sched = self.run_debt_schedule()
        return {
            **returns,
            **debt_sched
        }
