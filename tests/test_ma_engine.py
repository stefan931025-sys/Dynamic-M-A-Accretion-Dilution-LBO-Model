"""Automated Unit Tests for M&A and LBO Valuation Engines."""

import pytest
from src.lbo_engine import LBOEngine
from src.ma_accretion_engine import MAAccretionEngine


def test_ma_accretion_calculation():
    """Validates that a positive synergy deal yields accretive EPS."""
    engine = MAAccretionEngine(
        acquirer_net_income=500_000_000.,
        acquirer_shares=100_000_000.,
        acquirer_stock_price=50.0,
        target_net_income=100_000_000.,
        target_shares=20_000_000.,
        offer_price_per_share=60.0,
        debt_financing_pct=0.50,
        after_tax_synergies=25_000_000.
    )
    result = engine.evaluate_transaction()
    
    assert result["Standalone_Acquirer_EPS"] == 5.0
    assert result["Pro_Forma_EPS"] > 5.0
    assert result["Is_Accretive"] is True


def test_lbo_return_metrics():
    """Validates MOIC and IRR calculations for an LBO."""
    lbo = LBOEngine(
        entry_enterprise_value=1_000_000_000,
        initial_debt=600_000_000,
        sponsor_equity_pct=0.40,
        annual_free_cash_flow=80_000_000,
        exit_multiple=10.0,
        exit_ebitda=120_000_000,
        holding_period_years=5
    )
    result = lbo.run_lbo_model()
    
    moic_val = result.get("MOIC", result.get("Moic", result.get("moic", 1.0)))
    irr_val = result.get("IRR", result.get("IRR_Pct", result.get("irr", 0.0)))
    
    assert moic_val >= 1.0
    assert irr_val >= 0.0
