class LBOEngine:
    def __init__(
        self,
        purchase_price: float,
        ebitda: float,
        entry_multiple: float,
        leverage_ratio: float,
        sponsor_equity_pct: float
    ):
        self.purchase_price = purchase_price
        self.ebitda = ebitda
        self.entry_multiple = entry_multiple
        self.leverage_ratio = leverage_ratio
        self.sponsor_equity_pct = sponsor_equity_pct
        
        # Calculate capital structure based on leverage and sponsor equity
        self.debt = self.ebitda * self.leverage_ratio
        self.equity = self.purchase_price * self.sponsor_equity_pct

    def run_debt_schedule(self, holding_period_years: int = 5, annual_ebitda_growth: float = 0.08) -> dict:
        """Simulates annual EBITDA growth, cash flows, and debt paydown over the holding period."""
        current_ebitda = self.ebitda
        current_debt = self.debt
        fcf_list = []

        for year in range(1, holding_period_years + 1):
            current_ebitda *= (1 + annual_ebitda_growth)
            # Simplified FCF approximation (e.g., 50% of EBITDA after interest/tax/capex)
            fcf = current_ebitda * 0.50
            fcf_list.append(fcf)
            current_debt = max(0.0, current_debt - fcf)

        return {
            "Ending_Debt": current_debt,
            "Free_Cash_Flows": fcf_list
        }

    def calculate_returns(self, exit_multiple: float = 10.0, holding_period_years: int = 5) -> dict:
        """Calculates exit equity value, MOIC, and IRR for the LBO transaction."""
        projection = self.run_debt_schedule(holding_period_years=holding_period_years)
        final_ebitda = self.ebitda * ((1 + 0.08) ** holding_period_years)
        exit_enterprise_value = final_ebitda * exit_multiple
        exit_equity_value = exit_enterprise_value - projection["Ending_Debt"]

        moic = exit_equity_value / self.equity if self.equity > 0 else 0.0
        irr = (moic ** (1 / holding_period_years)) - 1 if moic > 0 else 0.0

        return {
            "Exit_Enterprise_Value": exit_enterprise_value,
            "Exit_Equity_Value": exit_equity_value,
            "MOIC": moic,
            "IRR": irr
        }
