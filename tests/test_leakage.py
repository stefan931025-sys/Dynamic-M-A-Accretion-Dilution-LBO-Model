"""
Temporal Data Leakage and Split Auditor (`tests/test_leakage.py`)
Enforces strict chronological ordering and prevents lookahead bias in backtests.
"""

import pandas as pd
import pytest
import numpy as np


def generate_mock_timeseries_data():
    """Generates a mock chronological pricing dataframe."""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    df = pd.DataFrame({
        "timestamp": dates,
        "feature_x": np.linspace(10, 110, 100),
        "target": np.random.normal(0, 1, 100)
    })
    return df


def time_series_train_test_split(df, test_size=0.2):
    """Performs a strict chronological split without shuffling."""
    split_idx = int(len(df) * (1 - test_size))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    return train, test


def test_temporal_ordering_and_no_leakage():
    """Asserts that test timestamps occur strictly after training timestamps."""
    df = generate_mock_timeseries_data()
    train, test = time_series_train_test_split(df, test_size=0.2)
    
    # 1. Verify strict chronological ordering
    assert train["timestamp"].is_monotonic_increasing, "Training set is not chronologically ordered."
    assert test["timestamp"].is_monotonic_increasing, "Test set is not chronologically ordered."
    
    # 2. Verify zero timestamp overlap (no leakage)
    max_train_time = train["timestamp"].max()
    min_test_time = test["timestamp"].min()
    
    assert max_train_time < min_test_time, (
        f"Data leakage detected! Max training timestamp ({max_train_time}) "
        f"is greater than or equal to min test timestamp ({min_test_time})."
    )
