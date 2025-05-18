
import yfinance as yf
import pandas as pd
import random

def generate_mock_data(num_exchanges=3, num_points=60, base_price=100.0, base_volume=1000):
    exchanges = {
        f"Exchange{chr(65+i)}": [base_price * (1 + random.uniform(-0.01, 0.01))]
        for i in range(num_exchanges)
    }
    volumes = []
    for t in range(num_points):
        vol = max(0, random.gauss(base_volume, base_volume * 0.1))
        volumes.append(vol)
        if t < num_points - 1:
            for name, prices in exchanges.items():
                current_price = prices[-1]
                next_price = current_price * (1 + random.gauss(0, 0.005))
                next_price = max(0.1, next_price)
                prices.append(next_price)
    return exchanges, volumes

def fetch_yahoo_data(symbol="AAPL", period="5d", interval="5m"):
    import yfinance as yf
    import pandas as pd

    try:
        symbol = symbol.upper().strip()
        df = yf.download(
            tickers=symbol,
            period=period,
            interval=interval,
            group_by="ticker",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if df.empty:
            print("⚠️ No data returned.")
            return pd.DataFrame()

        # 🔧 Flatten multi-index columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() for col in df.columns.values]

        # 🧽 Normalize columns by removing symbol prefix
        df.columns = [col.replace(f"{symbol}_", "") for col in df.columns]

        df.reset_index(inplace=True)
        return df

    except Exception as e:
        print(f"❌ Fetch error: {e}")
        return pd.DataFrame()
