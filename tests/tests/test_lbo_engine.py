import pytest
import pandas as pd
import numpy as np
from src.lbo_engine import LBOEngine


def test_lbo_engine_initialization():
    """Validates that LBOEngine initializes correctly with default financial assumptions."""
    engine = LBOEngine(
        purchase_price=500.0,
        ebitda=50.0,
        entry_multiple=10.0,
        leverage_ratio=4.0,
        sponsor_equity_pct=0.40
    )
    assert engine.purchase_price == 500.0
    assert engine.ebitda == 50.0
    assert engine.debt == 200.0
    assert engine.equity == 200.0


def test_debt_schedule_generation():
    """Validates that the debt schedule generates projected cash flows and debt paydown."""
    engine = LBOEngine(
        purchase_price=500.0,
        ebitda=50.0,
        entry_multiple=10.0,
        leverage_ratio=4.0,
        sponsor_equity_pct=0.40
    )
    
    projection = engine.run_debt_schedule(holding_period_years=5, annual_ebitda_growth=0.08)
    
    assert isinstance(projection, dict)
    assert "Ending_Debt" in projection
    assert "Free_Cash_Flows" in projection
    assert isinstance(projection["Free_Cash_Flows"], list)
    assert len(projection["Free_Cash_Flows"]) == 5


def test_returns_metrics():
    """Validates IRR and MOIC return calculations for the LBO transaction."""
    engine = LBOEngine(
        purchase_price=500.0,
        ebitda=50.0,
        entry_multiple=10.0,
        leverage_ratio=4.0,
        sponsor_equity_pct=0.40
    )
    
    metrics = engine.calculate_returns(exit_multiple=10.0, holding_period_years=5)
    
    assert isinstance(metrics, dict)
    assert "IRR" in metrics or "irr" in metrics
    assert "MOIC" in metrics or "moic" in metrics
    moic_val = metrics.get("MOIC", metrics.get("Moic", metrics.get("moic", 0.0)))
    assert isinstance(moic_val, float)
    assert moic_val > 0.0


def test_lbo_return_metrics():
    """Validates MOIC and IRR calculations for an LBO using detailed entry/exit parameters."""
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
    
    moic_val = result.get("MOIC", result.get("Moic", result.get("moic", 0.0)))
    irr_val = result.get("IRR", result.get("Irr", result.get("irr", 0.0)))
    
    assert moic_val >= 1.0
    assert irr_val >= 0.0
