# 🛢️ OilPulse — Oil Market Intelligence System

**Live Dashboard:** [oilpulse-soumyadeep.streamlit.app](https://oilpulse-soumyadeep.streamlit.app/)

An end-to-end ML pipeline that combines GARCH(1,1) volatility modeling with LSTM forecasting and regime classification to analyze oil market dynamics and their impact on Indian equities.

---

## The Problem

Oil price volatility drives billions in daily equity market movements across India — airlines, refiners, paint companies, and tire manufacturers all respond differently to crude price shocks. Yet most retail investors and analysts treat oil volatility as a single number (high or low), missing the critical insight that **different volatility regimes create systematically different winners and losers.**

OilPulse solves this by building a regime-aware intelligence system that tells you not just *how volatile* the market is, but *what kind of volatility* it is — and which stocks historically thrive or suffer in each state.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATA INGESTION                       │
│  Yahoo Finance API → Brent Crude + 14 NSE Stock Prices  │
│  17 years of daily data (2007–2024)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               STAGE 1: GARCH(1,1) ENGINE                │
│  • Extracts conditional volatility from oil returns     │
│  • Captures volatility clustering (β = 0.85–0.95)      │
│  • Output: Daily conditional variance series            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            STAGE 2: REGIME CLASSIFICATION                │
│  Quantile-based classification into 4 regimes:          │
│  🟢 LOW  │  🟡 MODERATE  │  🟠 HIGH  │  🔴 CRISIS     │
│  Historical stock performance mapped per regime         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              STAGE 3: LSTM FORECASTING                   │
│  • 12 engineered features from GARCH + market data      │
│  • 30-day sequence windows                              │
│  • Temporal train/test split (2007–2022 / 2023–2024)    │
│  • Zero lookahead bias                                  │
│  • Directional accuracy: 53% (2-year out-of-sample)     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            STAGE 4: LIVE DASHBOARD                       │
│  • Real-time Brent crude price via Yahoo Finance        │
│  • Live GARCH refit on updated data                     │
│  • 30-day volatility forecast visualization             │
│  • Regime-aware stock recommendations                   │
│  • News integration via NewsAPI                         │
└─────────────────────────────────────────────────────────┘
```

---

## Key Findings

| Finding | Detail |
|---------|--------|
| **BPCL wins in CRISIS regimes** | 70.2% win rate — refinery margin expansion during crude price shocks makes downstream refiners counter-intuitive crisis winners |
| **IndiGo loses across ALL regimes** | Airlines have inverse oil exposure — fuel costs dominate operating expenses regardless of volatility state |
| **LOW volatility ≠ safe** | Several stocks show compressed returns in LOW regimes — stable oil prices reduce the volatility premium that energy traders depend on |
| **Regime persistence** | GARCH β parameter of 0.85–0.95 confirms volatility shocks in oil markets persist for weeks to months — not mean-reverting quickly |

---

## Model Performance

| Metric | Value | Context |
|--------|-------|---------|
| Directional Accuracy | 53% | 2-year out-of-sample (2023–2024). Consistently beating 55% on commodity direction would be extraordinary — markets are near-efficient |
| MAE | 0.27 | Mean absolute error on normalized volatility predictions |
| Training Period | 2007–2022 | 15 years covering multiple market cycles including GFC, COVID, Ukraine war |
| Test Period | 2023–2024 | Strict temporal split — zero data leakage |
| Early Stopping | Epoch 26 | Stopped via validation loss monitoring to prevent overfitting |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Volatility Modeling | `arch` (GARCH), `statsmodels` |
| Deep Learning | TensorFlow / Keras (LSTM) |
| Data Processing | Pandas, NumPy |
| Data Source | Yahoo Finance (`yfinance`) |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Deployment | Streamlit Cloud |

---

## Stocks Analyzed

14 NSE-listed companies across oil-sensitive sectors:

**Upstream/Downstream:** ONGC, BPCL, HPCL, IOC, Reliance Industries

**Aviation:** IndiGo, SpiceJet

**Paint:** Asian Paints, Berger Paints

**Tires:** MRF, Apollo Tyres

**Logistics/Other:** Maruti Suzuki, Tata Motors, Adani Total Gas

---

## Project Structure

```
OilPulse/
├── app.py                  # Streamlit dashboard (1,241 lines)
├── oil_complete.csv        # Processed oil price + volatility data
├── stock_prices.csv        # 14 NSE stock price histories
├── stock_returns.csv       # Computed daily returns
├── combined_data.csv       # Merged dataset with regime labels
├── regime_performance.csv  # Win rates & mean returns by regime
├── lstm_features.csv       # Engineered features for LSTM
├── lstm_model.h5           # Trained LSTM model weights
├── scaler_X.pkl            # Feature scaler (MinMaxScaler)
├── scaler_y.pkl            # Target scaler (MinMaxScaler)
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version specification
└── License                 # All rights reserved
```

---

## Run Locally

```bash
# Clone the repository
git clone https://github.com/soumyadeep200223/OilPulse.git
cd OilPulse

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

---

## Why GARCH and Not Rolling Volatility?

Rolling standard deviation treats all observations equally — a shock from 30 days ago has the same weight as yesterday's shock. GARCH(1,1) solves this by weighting recent observations more heavily through the conditional variance equation:

**σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁**

In oil markets, the persistence parameter β typically falls between 0.85–0.95, meaning volatility shocks decay slowly — yesterday's turbulence strongly predicts today's. This is the econometric foundation that makes regime classification meaningful rather than arbitrary.

---

## Why 53% Accuracy Is Honest

Predicting the direction of commodity volatility changes over a 2-year out-of-sample window at 53% is a realistic result. Financial markets are near-efficient — any model consistently achieving 60%+ directional accuracy on unseen data would represent extraordinary alpha. The value of OilPulse is not in the point prediction but in the **regime classification system** that maps volatility states to historically validated stock behavior patterns.

---

## Future Roadmap (v2)

- [ ] Automated GARCH retraining on monthly schedule
- [ ] Forward-looking regime probability estimation
- [ ] Portfolio optimization layer — regime-conditional weight allocation
- [ ] Backtesting engine for regime-based trading strategies
- [ ] Additional commodities (Gold, Natural Gas)
- [ ] API endpoint for programmatic access

---

## Research Foundation

This project builds on a 4-stage econometric research framework analyzing oil price volatility transmission to corporate profitability across Indian energy and financial sectors (2000–2024), using EWMA, GARCH, panel regression with fixed effects, and ARIMA forecasting.

---

## Author

**Soumyadeep Paul**
BSc Economics (First Class) — University of Calcutta, 2024

📧 psoumyadeep22@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/soumyadeep-paul-ml/)
🌐 [Live Dashboard](https://oilpulse-soumyadeep.streamlit.app/)

---

## License

All rights reserved. See [License](./License) for details.
