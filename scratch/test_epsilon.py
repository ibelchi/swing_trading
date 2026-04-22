import yfinance as yf
import pandas as pd
import math

from src.strategies.pattern_classifier import PatternClassifier

def test_epsilon():
    for symbol in ["MSFT", "AAPL", "TSLA", "INTC", "F", "PFE"]:
        print(f"--- {symbol} ---")
        try:
            raw = yf.download(symbol, period="1y", auto_adjust=True, progress=False)
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = [col[0] if isinstance(col, tuple) else col for col in raw.columns]
            
            Close = raw["Close"]
            closes = Close.values
            price_range = float(Close.max() - Close.min())
            daily_volatility = float(Close.pct_change().abs().median())
            avg_price = float(Close.mean())
            atr_proxy = daily_volatility * avg_price
            
            epsilon = max(price_range * 0.05, atr_proxy * 20)
            
            def _perpendicular_distance(pt, line_start, line_end):
                x0, y0 = pt
                x1, y1 = line_start
                x2, y2 = line_end
                numerator = abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)
                denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
                if denominator == 0:
                    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
                return numerator / denominator

            def rdp_local(points, eps):
                dmax = 0.0
                index = 0
                end = len(points) - 1
                for i in range(1, end):
                    d = _perpendicular_distance(points[i], points[0], points[end])
                    if d > dmax:
                        index = i
                        dmax = d
                if dmax > eps:
                    result1 = rdp_local(points[:index+1], eps)
                    result2 = rdp_local(points[index:], eps)
                    return result1[:-1] + result2
                else:
                    return [points[0], points[-1]]

            pts = [(i, closes[i]) for i in range(len(closes))]
            max_iterations = 6
            iteration = 0
            current_eps = epsilon
            
            while iteration < max_iterations:
                key_points = rdp_local(pts, current_eps)
                print(f"Iter {iteration} EPS {current_eps:.2f} -> {len(key_points)} pivots")
                if len(key_points) <= 16:
                    break
                current_eps *= 1.5
                iteration += 1
        except Exception as e:
            print(f"Error {symbol}: {e}")

test_epsilon()
