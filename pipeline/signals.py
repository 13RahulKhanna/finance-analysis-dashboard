import pandas as pd


def compute_signals(df: pd.DataFrame, window: int):
    """Rolling mean vs close binary signal (1 = above mean, 0 otherwise)."""
    rolling_mean = df["close"].rolling(window=window).mean()
    signal = (df["close"] > rolling_mean).astype(int)
    return rolling_mean, signal


def build_metrics(df: pd.DataFrame, signal: pd.Series, config: dict, latency_ms: int):
    """Aggregate pipeline metrics including fields used for LLM interpretation only."""
    rows_processed = len(df)
    signal_rate = float(signal.mean())

    close = df["close"]
    avg_price = float(close.mean())
    rets = close.pct_change().dropna()
    volatility = float(rets.std()) if len(rets) else 0.0
    trend = "upward" if float(close.iloc[-1]) > float(close.iloc[0]) else "downward"
    buy_signals = int(signal.sum())
    sell_signals = int((signal == 0).sum())

    return {
        "version": config["version"],
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": latency_ms,
        "seed": config["seed"],
        "status": "success",
        "avg_price": round(avg_price, 4),
        "volatility": round(volatility, 6),
        "trend": trend,
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
    }
