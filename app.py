import streamlit as st
import pandas as pd
from data import generate_mock_data, fetch_yahoo_data
from exchange import Exchange
from sor import SmartOrderRouter
from strategies import vwap, twap, pov

st.title("Smart Order Routing Simulator")

mode = st.sidebar.selectbox("Data Mode", ["Synthetic Data", "Live Data"])
if mode == "Live Data":
    symbol = st.sidebar.text_input("Ticker Symbol", value="AAPL")
else:
    num_ex = st.sidebar.slider("Number of Exchanges", 2, 5, value=3)
    num_steps = st.sidebar.number_input("Time Steps (intervals)", min_value=1, value=60)

order_qty = st.sidebar.number_input("Order Quantity", min_value=1, value=10000)
side = st.sidebar.selectbox("Order Side", ["Buy", "Sell"])
algo = st.sidebar.selectbox("Execution Algorithm", ["VWAP", "TWAP", "POV"])
p_rate = None
if algo == "POV":
    p_rate = st.sidebar.slider("Participation Rate (%)", 1, 100, value=10)

if st.sidebar.button("Run Simulation"):
    if mode == "Live Data":
        data_df = fetch_yahoo_data(symbol)

        if data_df.empty:
            st.error("No data returned from Yahoo Finance.")
            st.stop()

        st.write("Fetched Yahoo Columns:", data_df.columns)

        if "Close" not in data_df.columns or "Volume" not in data_df.columns:
            st.error("Required columns missing from Yahoo Finance response.")
            st.stop()

        prices = pd.to_numeric(data_df["Close"], errors="coerce").dropna().tolist()
        volumes = pd.to_numeric(data_df["Volume"], errors="coerce").dropna().tolist()

        if not prices or not volumes:
            st.error("No valid data found.")
            st.stop()

        price_series = {
            "ExchangeA": prices,
            "ExchangeB": [p * 1.001 for p in prices],
            "ExchangeC": [p * 0.999 for p in prices],
        }
    else:
        price_series, volumes = generate_mock_data(num_exchanges=num_ex, num_points=num_steps)

    exchanges = [Exchange(name, prices[0]) for name, prices in price_series.items()]
    sor = SmartOrderRouter(exchanges)
    T = len(volumes)

    if algo == "VWAP":
        schedule = vwap.plan_vwap(order_qty, T)
    elif algo == "TWAP":
        schedule = twap.plan_twap(order_qty, T)
    elif algo == "POV":
        schedule = pov.plan_pov(order_qty, p_rate / 100.0, volumes)

    trades = []
    for t in range(T):
        for ex in exchanges:
            ex.update_price(price_series[ex.name][t] if t < len(price_series[ex.name]) else ex.price)
        qty = schedule[t] if t < len(schedule) else 0
        if qty > 0:
            ex_name, price, qty_exec = sor.route_order(qty, side)
            trades.append((t, ex_name, float(price), float(qty_exec)))

    if trades:
        trade_df = pd.DataFrame(trades, columns=["Time", "Exchange", "Price", "Quantity"])
        st.write("Executed Trades:", trade_df)
        avg_price = sum(p * q for _, _, p, q in trades) / order_qty
        st.write(f"Average Execution Price: **${avg_price:.2f}**")
    else:
        st.warning("No trades executed.")

    price_df = pd.DataFrame(price_series)
    st.line_chart(price_df)
