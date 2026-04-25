import yfinance as yf
import pandas as pd
import numpy as np

def calculate_correlation_matrix(
    symbols: list,
    period_days: int = 60
) -> dict:
    """
    Calculates the correlation matrix for a list of tickers based on daily returns.
    Returns the matrix, high correlation pairs, and an overall risk level.
    """
    if not symbols or len(symbols) < 2:
        return {
            "matrix": pd.DataFrame(),
            "high_corr_pairs": [],
            "avg_portfolio_correlation": 0,
            "warning_level": "LOW"
        }

    # Descarrega tots els tickers d'un cop (més eficient)
    try:
        data = yf.download(
            symbols,
            period=f"{period_days + 15}d",
            auto_adjust=True,
            progress=False,
            group_by='ticker'
        )
        
        # Extract Close prices
        if len(symbols) == 1:
            close_data = data['Close']
        else:
            # Handle multi-index columns from yfinance download
            close_data = pd.DataFrame()
            for sym in symbols:
                if sym in data.columns.levels[0]:
                    close_data[sym] = data[sym]['Close']
        
        close_data = close_data.tail(period_days)
    except Exception as e:
        print(f"Error downloading data for correlation: {e}")
        return {
            "matrix": pd.DataFrame(),
            "high_corr_pairs": [],
            "avg_portfolio_correlation": 0,
            "warning_level": "LOW"
        }

    # Elimina tickers sense dades
    close_data = close_data.dropna(axis=1, how="all")
    
    if close_data.empty or len(close_data.columns) < 2:
        return {
            "matrix": pd.DataFrame(),
            "high_corr_pairs": [],
            "avg_portfolio_correlation": 0,
            "warning_level": "LOW"
        }

    # Calcula retorns diaris (no preus absoluts)
    returns = close_data.pct_change().dropna()

    # Matriu de correlació
    corr_matrix = returns.corr().round(2)

    # Parells amb correlació alta (alerta)
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            val = corr_matrix.iloc[i, j]
            if not np.isnan(val) and val >= 0.75:
                high_corr_pairs.append({
                    "ticker_a": corr_matrix.columns[i],
                    "ticker_b": corr_matrix.columns[j],
                    "correlation": float(val),
                    "warning": (
                        "🔴 Very high" if val >= 0.90 else
                        "🟠 High"
                    )
                })

    # Concentració sectorial (proxy via correlació)
    # Filter out diagonal elements (self-correlation)
    mask = ~np.eye(len(corr_matrix), dtype=bool)
    if mask.any():
        avg_corr = corr_matrix.values[mask].mean()
    else:
        avg_corr = 0

    return {
        "matrix": corr_matrix,
        "high_corr_pairs": sorted(
            high_corr_pairs,
            key=lambda x: x["correlation"],
            reverse=True
        ),
        "avg_portfolio_correlation": round(float(avg_corr), 2) if not np.isnan(avg_corr) else 0.0,
        "warning_level": (
            "HIGH" if avg_corr > 0.70 else
            "MEDIUM" if avg_corr > 0.50 else
            "LOW"
        )
    }
