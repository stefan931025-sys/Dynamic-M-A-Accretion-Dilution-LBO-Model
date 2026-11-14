#!/usr/bin/env python3
"""
Quantitative M&A Accretion/Dilution & LBO Valuation Engine (`lbo_ma_engine.py`)
Engineered to evaluate buy-side acquisition scenarios, model pro-forma EPS accretion/dilution,
and simulate LBO debt waterfall returns across vectorized sensitivity matrices.
"""

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class AcquisitionParams:
    acquirer_net_income: float
    target_net_income: float
    acquirer_shares_outstanding: float
    acquirer_share_price: float
    total_purchase_price: float
    cash_consideration: float
    new_debt_raised: float
    interest_rate_debt: float
    tax_rate: float
    pre_tax_synergies: float


@dataclass
class LBOParams:
    purchase_price: float
    initial_sponsor_equity: float
    initial_debt: float
    exit_equity_value: float
    holding_period_years: float
    annual_fcf_stream: list[float]


class QuantitativeValuationEngine:
    """Core engine for M&A accretion/dilution analysis and LBO return waterfalls."""

    @staticmethod
    def calculate_pro_forma_eps(params: AcquisitionParams) -> dict[str, float]:
        """
        Calculates Pro-Forma EPS Accretion/Dilution based on formal specifications:
        Pro-Forma EPS = (Acquirer NI + Target NI + After-Tax Synergies - After-Tax Interest Expense) 
                        / (Acquirer Shares Outstanding + New Shares Issued)
        """
        # 1. After-Tax Interest Expense on new debt raised
        after_tax_interest = (params.new_debt_raised * params.interest_rate_debt) * (1.0 - params.tax_rate)

        # 2. After-Tax Synergies
        after_tax_synergies = params.pre_tax_synergies * (1.0 - params.tax_rate)

        # 3. New Shares Issued for stock consideration portion
        stock_consideration = params.total_purchase_price - params.cash_consideration
        new_shares_issued = stock_consideration / params.acquirer_share_price

        # 4. Numerator: Pro-Forma Net Income
        pro_forma_net_income = (
            params.acquirer_net_income
            + params.target_net_income
            + after_tax_synergies
            - after_tax_interest
        )

        # 5. Denominator: Total Pro-Forma Shares
        pro_forma_shares = params.acquirer_shares_outstanding + new_shares_issued

        # 6. EPS Calculations
        standalone_acquirer_eps = params.acquirer_net_income / params.acquirer_shares_outstanding
        pro_forma_eps = pro_forma_net_income / pro_forma_shares
        eps_delta = pro_forma_eps - standalone_acquirer_eps
        accretion_percentage = (eps_delta / standalone_acquirer_eps) * 100.0

        return {
            "standalone_acquirer_eps": round(standalone_acquirer_eps, 4),
            "pro_forma_eps": round(pro_forma_eps, 4),
            "eps_delta": round(eps_delta, 4),
            "accretion_percentage": round(accretion_percentage, 2),
            "new_shares_issued": round(new_shares_issued, 2),
            "after_tax_interest": round(after_tax_interest, 2),
            "after_tax_synergies": round(after_tax_synergies, 2),
        }

    @staticmethod
    def calculate_lbo_returns(params: LBOParams) -> dict[str, float]:
        """
        Calculates Sponsor MoIC and IRR according to specifications:
        MoIC = Exit Equity Value / Sponsor Initial Equity Invested
        Sponsor IRR = (MoIC) ** (1 / t) - 1
        """
        if params.initial_sponsor_equity <= 0:
            raise ValueError("Sponsor initial equity must be greater than zero.")

        moic = params.exit_equity_value / params.initial_sponsor_equity
        irr = (moic ** (1.0 / params.holding_period_years)) - 1.0

        return {
            "moic": round(moic, 4),
            "irr_percentage": round(irr * 100.0, 2),
        }

    @staticmethod
    def run_vectorized_purchase_multiple_sensitivity(
        base_params: AcquisitionParams, purchase_multiples: np.ndarray, target_earnings: float
    ) -> pd.DataFrame:
        """Generates a vectorized sensitivity matrix across varying purchase multiples."""
        results = []
        for mult in purchase_multiples:
            adjusted_price = target_earnings * mult
            # Assume cash consideration scales or stays fixed, adjust new debt accordingly
            adjusted_debt = max(0.0, adjusted_price - base_params.cash_consideration)
            
            scenario = AcquisitionParams(
                acquirer_net_income=base_params.acquirer_net_income,
                target_net_income=base_params.target_net_income,
                acquirer_shares_outstanding=base_params.acquirer_shares_outstanding,
                acquirer_share_price=base_params.acquirer_share_price,
                total_purchase_price=adjusted_price,
                cash_consideration=base_params.cash_consideration,
                new_debt_raised=adjusted_debt,
                interest_rate_debt=base_params.interest_rate_debt,
                tax_rate=base_params.tax_rate,
                pre_tax_synergies=base_params.pre_tax_synergies,
            )
            res = QuantitativeValuationEngine.calculate_pro_forma_eps(scenario)
            results.append({
                "Purchase Multiple": mult,
                "Total Purchase Price": adjusted_price,
                "Pro-Forma EPS": res["pro_forma_eps"],
                "Accretion (%)": res["accretion_percentage"],
            })
            
        return pd.DataFrame(results)


if __name__ == "__main__":
    # Example Execution / Validation Run
    acq_test = AcquisitionParams(
        acquirer_net_income=500_000_000.0,
        target_net_income=100_000_000.0,
        acquirer_shares_outstanding=200_000_000.0,
        acquirer_share_price=25.0,
        total_purchase_price=1_200_000_000.0,
        cash_consideration=400_000_000.0,
        new_debt_raised=800_000_000.0,
        interest_rate_debt=0.065,
        tax_rate=0.25,
        pre_tax_synergies=30_000_000.0,
    )

    eps_results = QuantitativeValuationEngine.calculate_pro_forma_eps(acq_test)
    print("--- M&A Accretion/Dilution Results ---")
    for k, v in eps_results.items():
        print(f"{k}: {v}")

    lbo_test = LBOParams(
        purchase_price=2_000_000_000.0,
        initial_sponsor_equity=600_000_000.0,
        initial_debt=1_400_000_000.0,
        exit_equity_value=1_800_000_000.0,
        holding_period_years=5.0,
        annual_fcf_stream=[100m, 120m, 140m, 160m, 180m] # placeholder or numerical sequence
    ) if False else LBOParams(
        purchase_price=2_000_000_000.0,
        initial_sponsor_equity=600_000_000.0,
        initial_debt=1_400_000_000.0,
        exit_equity_value=1_800_000_000.0,
        holding_period_years=5.0,
        annual_fcf_stream=[100_000_000.0, 120_000_000.0, 140_000_000.0, 160_000_000.0, 180_000_000.0]
    )

    lbo_results = QuantitativeValuationEngine.calculate_lbo_returns(lbo_test)
    print("\n--- LBO Returns Waterfall Results ---")
    for k, v in lbo_results.items():
        print(f"{k}: {v}")
