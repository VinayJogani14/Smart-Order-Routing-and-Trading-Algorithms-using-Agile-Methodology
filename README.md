# AgileSmartSOR

**AgileSmartSOR** is an educational Smart Order Routing (SOR) simulator that models how institutional order execution algorithms operate across multiple exchanges. Designed for students, researchers, and fintech developers, this project simulates the mechanics of VWAP, TWAP, and POV algorithms using both synthetic and live market data.

---

## 🚀 Features

- **Smart Order Routing Engine** to simulate agency order execution across multiple exchanges
- **VWAP, TWAP, and POV algorithms** implemented in Python
- **Live market data integration** using Yahoo Finance (via `yfinance`)
- **Synthetic data generation** for testing execution strategies offline
- **Interactive GUI** built with Streamlit
- **Modular structure** using Agile-friendly architecture

---

## 🧱 Project Structure

```
AgileSmartSOR/
├── app.py                  # Main Streamlit application
├── data.py                 # Yahoo data fetcher and mock data generator
├── exchange.py             # Exchange class with price updating
├── sor.py                  # Smart Order Router logic
├── strategies/             # Execution algorithms
│   ├── vwap.py
│   ├── twap.py
│   └── pov.py
```

---

## ⚙️ Installation

```bash
git clone https://github.com/VinayJogani14/AgileSmartSOR.git
cd AgileSmartSOR
pip install streamlit yfinance pandas
```

---

## ▶️ Usage

Launch the app:

```bash
streamlit run app.py
```

Configure simulation options from the sidebar:
- Select **Data Mode**: Live or Synthetic
- Choose **Execution Algorithm**: VWAP, TWAP, POV
- Set order quantity and side (Buy/Sell)
- Run the simulation and view trade logs and charts

---

## 📊 Execution Algorithms

- **VWAP (Volume-Weighted Average Price)**: Splits order proportional to market volume.
- **TWAP (Time-Weighted Average Price)**: Splits order evenly across time steps.
- **POV (Percent of Volume)**: Executes a dynamic percent of live market volume.

---

## 📦 Future Enhancements

- Order book simulation
- Execution cost models
- Live price refresh with real-time feed
- Interactive parameter tuning
- Trade analytics dashboard


