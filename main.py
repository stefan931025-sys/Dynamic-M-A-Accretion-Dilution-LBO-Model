from src.data_loader import CorporateDataLoader
from src.lbo_engine import LBOEngine
from src.ma_accretion_engine import MAAccretionEngine

if __name__ == "__main__":
    print("--- INITIATING CORPORATE VALUATION & M&A ENGINE ---")

    # 1. Fetch live market metrics using yfinance
    loader = CorporateDataLoader("MSFT")
    market_data = loader.fetch_market_metrics()
    print(
        f"\nLive Acquirer Data ({market_data['ticker']}): Price = ${market_data['stock_price']:,.2f}"
    )

    # 2. Run M&A Accretion Evaluation
    ma_engine = MAAccretionEngine(
        acquirer_net_income=72_000_000_000,
        acquirer_shares=7_400_000_000,
        acquirer_stock_price=market_data["stock_price"],
        target_net_income=5_000_000_000,
        target_shares=800_000_000,
        offer_price_per_share=90.0,
        debt_financing_pct=0.70,
        after_tax_synergies=1_200_000_000,
    )
    ma_results = ma_engine.evaluate_transaction()

    print("\n[M&A Pro-Forma Accretion/Dilution Results]")
    for k, v in ma_results.items():
        print(f"  {k}: {v}")

    # 3. Run LBO Return Simulation
    lbo_engine = LBOEngine(
        entry_enterprise_value=2_500_000_000,
        initial_debt=1_500_000_000,
        sponsor_equity_pct=0.40,
        annual_free_cash_flow=200_000_000,
        exit_multiple=12.0,
        exit_ebitda=280_000_000,
        holding_period_years=5,
    )
    lbo_results = lbo_engine.run_lbo_model()

    print("\n[LBO Return & IRR Analysis]")
    for k, v in lbo_results.items():
        print(f"  {k}: {v}")
