"""
Corporate Data Ingestion Module
Fetches live market data, share counts, and pricing for acquirers and targets via yfinance.
"""

from typing import Dict
import yfinance as yf


class CorporateDataLoader:
    """Retrieves live equity market data for financial modeling."""

    def __init__(self, ticker: str):
        self.ticker_symbol = ticker.upper()
        self.stock = yf.Ticker(self.ticker_symbol)

    def fetch_market_metrics(self) -> Dict[str, float]:
        """Extracts current stock price, shares outstanding, and market capitalization."""
        try:
            info = self.stock.info
            stock_price = (
                info.get("currentPrice")
                or info.get("regularMarketPrice")
                or info.get("previousClose")
                or 100.0
            )
            shares_outstanding = info.get("sharesOutstanding") or 1_000_000_000
            market_cap = stock_price * shares_outstanding

            return {
                "ticker": self.ticker_symbol,
                "stock_price": float(stock_price),
                "shares_outstanding": float(shares_outstanding),
                "market_cap": float(market_cap),
            }
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch data for {self.ticker_symbol}: {str(e)}"
            )
