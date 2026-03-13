import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import urllib.request
import xml.etree.ElementTree as ET
def get_latest_oil_news():
    try:
        api_key = "bcf1e4a7be1843129f9d5e92cf207e01"
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q=oil+crude+OPEC&"
            f"language=en&"
            f"sortBy=publishedAt&"
            f"pageSize=5&"
            f"apiKey={api_key}"
        )
        with urllib.request.urlopen(url, timeout=5) as r:
            import json
            data = json.loads(r.read().decode())
        articles = data.get("articles", [])
        return [
            {
                "title": a["title"],
                "link": a["url"],
                "source": a["source"]["name"]
            }
            for a in articles[:5]
        ]
    except:
        return [{"title": "News feed unavailable", 
                 "link": "#", 
                 "source": ""}]
st.set_page_config(page_title = "OilPulse",layout = 'wide')
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Base */
.stApp {
    background-color: #0a0e17;
    color: #e2e8f0;
    font-family: 'Space Grotesk', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1220;
    border-right: 1px solid #1f2d45;
}
[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem;
}

/* All text */
p, div, span, label {
    font-family: 'Space Grotesk', sans-serif;
}

/* Headers */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    color: #ffffff !important;
    letter-spacing: -0.02em;
}
h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    letter-spacing: -0.01em;
    border-bottom: 1px solid #1f2d45;
    padding-bottom: 8px;
}
h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: #cbd5e0 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #1f2d45;
    border-radius: 10px;
    padding: 20px;
}
[data-testid="stMetric"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #718096 !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    color: #ffffff !important;
    font-weight: 600;
}

/* Selectbox */
[data-testid="stSelectbox"] {
    font-family: 'JetBrains Mono', monospace;
}

/* Info/Success/Warning/Error boxes */
.stAlert {
    border-radius: 8px;
    border: none;
    font-family: 'Space Grotesk', sans-serif;
}

/* Divider */
hr {
    border-color: #1f2d45;
    margin: 24px 0;
}

/* Plotly charts border */
.js-plotly-plot {
    border-radius: 10px;
    border: 1px solid #1f2d45;
}
/* Fix white top bar */
[data-testid="stHeader"] {
    background-color: #0a0e17;
    border-bottom: 1px solid #1f2d45;
}

/* Fix sidebar navigation text color */
[data-testid="stSidebar"] .stRadio label p {
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Fix selected radio option */
[data-testid="stSidebar"] .stRadio label {
    color: #e2e8f0 !important;
}

/* Fix sidebar collapse arrow */
[data-testid="collapsedControl"] {
    background-color: #0d1220;
    border: 1px solid #1f2d45;
    color: #e2e8f0;
}
[data-testid="collapsedControl"] svg {
    fill: #e2e8f0 !important;
}

/* Fix sidebar toggle button */
button[kind="header"] {
    background-color: #0d1220 !important;
    color: #e2e8f0 !important;
}

/* Fix any remaining white backgrounds */
.stDeployButton {
    display: none;
}
header[data-testid="stHeader"] {
    background: #0a0e17 !important;
}
</style>
""", unsafe_allow_html=True)
#load data
oil_data = pd.read_csv('oil_complete.csv', parse_dates=['Date'])
oil_data['regimes'] = oil_data['regimes'].str.strip()
perf = pd.read_csv('regime_performance.csv')
#sidebar
last = oil_data.iloc[-1]
regime_emoji = {"LOW": "🟢", "ELEVATED": "🟡", "HIGH": "🟠", "CRISIS": "🔴"}
current_regime = last['regimes']
st.sidebar.markdown("""
<div style='
    font-family: JetBrains Mono, monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #f5a623;
    letter-spacing: 0.05em;
    padding: 8px 0 4px 0;
'>🛢️ OilPulse</div>
<div style='
    font-family: JetBrains Mono, monospace;
    font-size: 0.65rem;
    color: #4a5568;
    margin-bottom: 16px;
'>v1.0 · Data through Dec 2024</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
regime_colors = {
    "LOW": "#00d68f",
    "ELEVATED": "#f5a623",
    "HIGH": "#f6882d",
    "CRISIS": "#e53e3e"
}
badge_color = regime_colors.get(current_regime, "#718096")

st.sidebar.markdown(f"""
<div style='
    display: inline-block;
    background: {badge_color}22;
    border: 1px solid {badge_color};
    color: {badge_color};
    font-family: JetBrains Mono, monospace;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 4px;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
'>{current_regime} REGIME</div>
<div style='
    font-family: JetBrains Mono, monospace;
    font-size: 0.65rem;
    color: #4a5568;
    margin-bottom: 8px;
'>As of Dec 2024</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<style>
div[role="radiogroup"] label {
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
}
div[role="radiogroup"] label p {
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)
# PERSISTENT TOP HEADER — shows on every page
st.markdown("""
<div style='
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: #111827;
    border: 1px solid #1f2d45;
    border-radius: 12px;
    margin-bottom: 24px;
'>
    <div>
        <div style='
            font-family: JetBrains Mono, monospace;
            font-size: 1.6rem;
            font-weight: 700;
            color: #f5a623;
            letter-spacing: 0.05em;
        '>🛢️ OilPulse</div>
        <div style='
            font-family: JetBrains Mono, monospace;
            font-size: 0.7rem;
            color: #4a5568;
            margin-top: 2px;
        '>Oil Market Intelligence · GARCH + LSTM + Regime Classification</div>
    </div>
    <div style='text-align: right;'>
        <div style='
            font-family: JetBrains Mono, monospace;
            font-size: 0.7rem;
            color: #718096;
        '>Built by Soumyadeep Paul</div>
        <div style='
            font-family: JetBrains Mono, monospace;
            font-size: 0.65rem;
            color: #4a5568;
            margin-top: 2px;
        '>Economics → ML · 2007–2024</div>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigate",[
    "📊 Market Overview",
    "📈 LSTM Forecast",
    "🏦 Stock Performance",
    "🔬 Model Info"
])

#page routing
if page == "📊 Market Overview" :
    
    st.title("📊 Market Overview")
    st.markdown("*BRENT Crude Oil · GARCH Volatility · Regime Classification · 2007–2024*")

    # TOP METRICS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Last Oil Price",
        value=f"${last['Close']:.2f}",
        delta=f"{last['return']:.2f}% daily return"
    )
    col2.metric(
        label="GARCH Volatility",
        value=f"{last['garch_vol']:.3f}"
    )
    col3.metric(
        label="Current Regime",
        value=current_regime
    )
    col4.metric(
        label="Data Period",
        value="2007-2024"
    )

    st.markdown("---")

    # OIL PRICE CHART
    st.subheader("BRENT Oil Price — Colored by Volatility Regime")

    COLORS = {
        "LOW": "#00d68f",
        "ELEVATED": "#f5a623",
        "HIGH": "#f6882d",
        "CRISIS": "#e53e3e"
    }

    fig = go.Figure()

    for regime in ["LOW", "ELEVATED", "HIGH", "CRISIS"]:
        mask = oil_data["regimes"] == regime
        fig.add_trace(go.Scatter(
            x=oil_data.loc[mask, "Date"],
            y=oil_data.loc[mask, "Close"],
            mode="markers",
            marker=dict(color=COLORS[regime], size=2),
            name=regime
        ))

    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="USD per barrel",
        legend_title="Regime",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # GARCH VOLATILITY CHART
    st.subheader("GARCH Conditional Volatility Over Time")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=oil_data["Date"],
        y=oil_data["garch_vol"],
        mode="lines",
        line=dict(color="#4299e1", width=1),
        fill="tozeroy",
        fillcolor="rgba(66,153,225,0.1)",
        name="GARCH Vol"
    ))
    fig2.update_layout(
        height=300,
        xaxis_title="Date",
        yaxis_title="Conditional Volatility",
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # REGIME DISTRIBUTION
    st.subheader("Regime Distribution — 17 Years")

    counts = oil_data["regimes"].value_counts()
    col1, col2, col3, col4 = st.columns(4)

    for col, regime in zip([col1, col2, col3, col4],
                           ["LOW", "ELEVATED", "HIGH", "CRISIS"]):
        pct = counts.get(regime, 0) / len(oil_data) * 100
        col.metric(
            regime,
            f"{pct:.1f}%",
            f"{counts.get(regime, 0):,} days"
        )
    st.markdown("---")
    st.subheader("📰 Latest Oil Market News")
    news = get_latest_oil_news()
    for item in news:
        st.markdown(
            f"🔹 [{item['title']}]({item['link']}) "
            f"*— {item.get('source', '')}*"
        )

   
elif page == "🏦 Stock Performance":
    st.title("🏦 Stock Performance by Regime")
    st.markdown("*14 NSE stocks · 4 volatility regimes · Win rate & mean return · 2007–2024*")

    # REGIME SELECTOR
    selected = st.selectbox(
        "Select regime to highlight",
        ["ALL", "LOW", "ELEVATED", "HIGH", "CRISIS"]
    )

    st.markdown("---")
    # REGIME SPECIFIC RANKING
    if selected != "ALL":
        st.subheader(f"📊 Stock Rankings in {selected} Regime")

        regime_data = perf[perf["regime"] == selected].copy()
        regime_data = regime_data.sort_values("win_rate", ascending=True)

        col1, col2 = st.columns(2)

        with col1:
            fig_bar = go.Figure(go.Bar(
                x=regime_data["win_rate"],
                y=regime_data["stock"],
                orientation="h",
                marker=dict(
                    color=regime_data["win_rate"],
                    colorscale=[
                        [0, "#7a1a1a"],
                        [0.5, "#2a2a0a"],
                        [1, "#00d68f"]
                    ],
                    showscale=False
                ),
                text=[f"{v:.1f}%" for v in regime_data["win_rate"]],
                textposition="outside",
                hovertemplate="%{y}: %{x:.1f}%<extra></extra>"
            ))

            fig_bar.add_vline(
                x=50,
                line=dict(color="#718096", width=1, dash="dot"),
                annotation_text="50% baseline"
            )

            fig_bar.update_layout(
                height=450,
                title="Win Rate (%)",
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font_color="#fafafa",
                xaxis_title="Win Rate %",
                yaxis_title=None
            )

            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            regime_data_mr = perf[perf["regime"] == selected].copy()
            regime_data_mr = regime_data_mr.sort_values(
                "mean_return", ascending=True
            )

            fig_bar2 = go.Figure(go.Bar(
                x=regime_data_mr["mean_return"],
                y=regime_data_mr["stock"],
                orientation="h",
                marker=dict(
                    color=regime_data_mr["mean_return"],
                    colorscale=[
                        [0, "#7a1a1a"],
                        [0.5, "#0a2a2a"],
                        [1, "#00d68f"]
                    ],
                    showscale=False
                ),
                text=[f"{v:.2f}%" for v in regime_data_mr["mean_return"]],
                textposition="outside",
                hovertemplate="%{y}: %{x:.2f}%<extra></extra>"
            ))

            fig_bar2.update_layout(
                height=450,
                title="Mean Daily Return (%)",
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font_color="#fafafa",
                xaxis_title="Mean Return %",
                yaxis_title=None
            )

            st.plotly_chart(fig_bar2, use_container_width=True)

        st.markdown("---")

    # WIN RATE HEATMAP
    st.subheader("Win Rate (%) — How often each stock gives positive returns")

    stocks = ["ONGC", "Reliance", "BPCL", "IndiGo", "Maruti",
              "Mahindra", "Asian Paints", "Pidilite", "HUL",
              "ITC", "HDFC Bank", "SBI", "TCS", "Infosys"]

    regimes = ["LOW", "ELEVATED", "HIGH", "CRISIS"]

    pivot_wr = perf.pivot_table(
        values="win_rate",
        index="stock",
        columns="regime"
    ).reindex(index=stocks, columns=regimes)

    fig = go.Figure(go.Heatmap(
        z=pivot_wr.values,
        x=regimes,
        y=stocks,
        colorscale=[
            [0, "#2a0a0a"],
            [0.4, "#7a1a1a"],
            [0.6, "#0a2a1a"],
            [1, "#00d68f"]
        ],
        zmid=50,
        text=[[f"{v:.1f}%" for v in row] for row in pivot_wr.values],
        texttemplate="%{text}",
        textfont=dict(size=11),
        hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>Win Rate: %{z:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        height=500,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa",
        xaxis_title="Volatility Regime",
        yaxis_title="Stock"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # MEAN RETURN HEATMAP
    st.subheader("Mean Daily Return (%) — Average return per regime")

    pivot_mr = perf.pivot_table(
        values="mean_return",
        index="stock",
        columns="regime"
    ).reindex(index=stocks, columns=regimes)

    fig2 = go.Figure(go.Heatmap(
        z=pivot_mr.values,
        x=regimes,
        y=stocks,
        colorscale=[
            [0, "#2a0a0a"],
            [0.3, "#1a1a2a"],
            [0.7, "#0a2a2a"],
            [1, "#00d68f"]
        ],
        text=[[f"{v:.2f}" for v in row] for row in pivot_mr.values],
        texttemplate="%{text}",
        textfont=dict(size=11),
        hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>Mean Return: %{z:.2f}%<extra></extra>"
    ))

    fig2.update_layout(
        height=500,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa",
        xaxis_title="Volatility Regime",
        yaxis_title="Stock"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # KEY INSIGHTS
    st.subheader("📌 Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**IndiGo anomaly:** Lowest win rates across "
            "ALL regimes (20–39%). Airlines have inverse "
            "oil exposure — high oil volatility crushes margins."
        )
        st.success(
            "**CRISIS winners:** BPCL (70.2% win rate) and "
            "Reliance (66.5%) dominate in Crisis. Refiners "
            "benefit from crude-product spread expansion."
        )

    with col2:
        st.success(
            "**Defensive plays in LOW regime:** Asian Paints "
            "(67.6%), TCS (63.3%), Pidilite (63%) — "
            "consumer and IT stocks thrive in calm markets."
        )
        st.warning(
            "**Regime matters more than stock picking:** "
            "The same stock can have 20% win rate in one "
            "regime and 67% in another. Regime first, "
            "stock second."
        )
elif page == "📈 LSTM Forecast":
    st.title("📈 LSTM Volatility Forecast")
    st.markdown("*GARCH-informed LSTM · 30-day volatility prediction · Temporal train/test split*")

    # MODEL METRICS
    st.subheader("Model Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Direction Accuracy",
        value="53.0%",
        delta="vs 50% random baseline"
    )
    col2.metric(
        label="MAE",
        value="0.27",
        delta="Mean Absolute Error"
    )
    col3.metric(
        label="Training Stopped",
        value="Epoch 26",
        delta="Early stopping"
    )
    col4.metric(
        label="Train/Test Split",
        value="Temporal",
        delta="No lookahead bias"
    )

    st.markdown("---")

    # TRAIN TEST SPLIT VISUALIZATION
    st.subheader("GARCH Volatility — Training vs Test Period")

    features = pd.read_csv("lstm_features.csv", parse_dates=["Date"])

    split_date = pd.Timestamp("2023-01-01")
    train = features[features["Date"] < split_date]
    test = features[features["Date"] >= split_date]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=train["Date"],
        y=train["garch_vol"],
        mode="lines",
        name="Training Data (2007–2022)",
        line=dict(color="#4299e1", width=1),
        fill="tozeroy",
        fillcolor="rgba(66,153,225,0.08)"
    ))

    fig.add_trace(go.Scatter(
        x=test["Date"],
        y=test["garch_vol"],
        mode="lines",
        name="Test Data (2023–2024)",
        line=dict(color="#00d68f", width=1),
        fill="tozeroy",
        fillcolor="rgba(0,214,143,0.08)"
    ))

    fig.add_vline(
        x=str(split_date.date()),
        line=dict(color="#f5a623", width=2, dash="dot")
    )

    fig.add_annotation(
        x=str(split_date.date()),
        y=features["garch_vol"].max(),
        text="Train/Test Split — Jan 2023",
        showarrow=False,
        font=dict(color="#f5a623", size=11),
        bgcolor="#0e1117",
        bordercolor="#f5a623"
    )

    fig.update_layout(
        height=400,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa",
        xaxis_title="Date",
        yaxis_title="Conditional Volatility",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#fafafa")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # FEATURE IMPORTANCE
    st.subheader("Feature Correlation with GARCH Volatility")

    feature_cols = [c for c in features.columns if c != "Date"]
    corrs = features[feature_cols].corrwith(
        features["garch_vol"]
    ).abs().sort_values(ascending=True)

    fig2 = go.Figure(go.Bar(
        x=corrs.values,
        y=corrs.index,
        orientation="h",
        marker=dict(
            color=corrs.values,
            colorscale=[
                [0, "#1f2d45"],
                [0.5, "#4299e1"],
                [1, "#00d68f"]
            ],
            showscale=False
        ),
        hovertemplate="%{y}: %{x:.3f}<extra></extra>"
    ))

    fig2.update_layout(
        height=350,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa",
        xaxis_title="Absolute Correlation",
        title="Higher = more predictive of volatility"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # WHY GARCH THEN LSTM
    st.subheader("Why GARCH → LSTM?")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**The GARCH layer** captures volatility "
            "clustering — high volatility days tend to "
            "follow each other. Raw returns are "
            "unpredictable. Conditional volatility has "
            "memory. This is the econometrics foundation."
        )

    with col2:
        st.success(
            "**The LSTM layer** processes 30-day sequences "
            "of GARCH volatility + lags + momentum. It "
            "learns non-linear transition patterns between "
            "regimes — something GARCH alone cannot capture."
        )

    st.markdown("---")

    # INTERVIEW TALKING POINT
    st.subheader("The Story in One Paragraph")

    st.warning(
        "Built a two-stage volatility system. Stage one: "
        "GARCH(1,1) extracts conditional volatility from "
        "17 years of BRENT data - this is the fundamental feature engineering step that captures volatility clustering."
        " Stage two: LSTM processes "
        "30-day sequences of GARCH outputs to learn "
        "non-linear regime transition patterns. Strict "
        "temporal train/test split prevents lookahead bias. "
        "53% directional accuracy is modest but the "
        "regime classifier built on top creates actionable "
        "stock selection signals backed by 17 years of "
        "historical win rates across 14 Indian equities."
    )
elif page == "🔬 Model Info":
    st.title("🔬 Model Architecture & Pipeline")
    st.markdown("*End-to-end volatility intelligence system*")

    st.markdown("---")

    # PIPELINE STAGES
    st.subheader("The 5-Stage Pipeline")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.info(
            "**01**\n\n"
            "**Raw Oil Returns**\n\n"
            "BRENT daily returns\n"
            "2007–2024\n"
            "4,331 observations"
        )
    with col2:
        st.info(
            "**02**\n\n"
            "**GARCH(1,1)**\n\n"
            "Conditional volatility\n"
            "Captures clustering\n"
            "σ²t = ω + αε² + βσ²"
        )
    with col3:
        st.info(
            "**03**\n\n"
            "**Feature Engineering**\n\n"
            "12 features\n"
            "Lags: 1,5,10,21 days\n"
            "Momentum + vol ratio"
        )
    with col4:
        st.info(
            "**04**\n\n"
            "**LSTM Model**\n\n"
            "30-day sequences\n"
            "Temporal split\n"
            "53% direction accuracy"
        )
    with col5:
        st.info(
            "**05**\n\n"
            "**Regime Classifier**\n\n"
            "4 states\n"
            "14 NSE stocks\n"
            "Win rate per regime"
        )

    st.markdown("---")

    # DATASET STATS
    st.subheader("Dataset Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Observations", "4,331", "Daily oil prices")
    col2.metric("Study Period", "17 Years", "Jul 2007 – Dec 2024")
    col3.metric("Stocks Tracked", "14", "NSE-listed equities")
    col4.metric("Volatility Regimes", "4", "LOW / ELEVATED / HIGH / CRISIS")

    st.markdown("---")

    # GARCH EXPLANATION
    st.subheader("Why GARCH?")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            "**Volatility clustering is real.**\n\n"
            "In oil markets, large price moves tend to "
            "be followed by more large moves. Simple "
            "rolling standard deviation ignores this. "
            "GARCH explicitly models it.\n\n"
            "The β parameter in oil markets is typically "
            "0.85–0.95 — meaning volatility shocks "
            "are highly persistent."
        )

    with col2:
        st.success(
            "**Why not just use rolling std?**\n\n"
            "Rolling std treats all days in the window "
            "equally. GARCH weights recent observations "
            "more heavily — yesterday's shock matters "
            "more than last month's.\n\n"
            "This makes GARCH conditional volatility "
            "a richer feature for the LSTM than any "
            "simple rolling measure."
        )

    st.markdown("---")

    # MODEL DESIGN DECISIONS
    st.subheader("Key Design Decisions")

    st.warning(
        "**Temporal train/test split — not random.**\n\n"
        "Random splitting in time series causes lookahead "
        "bias — the model sees future data during training. "
        "We split at January 2023. Everything before trains "
        "the model. Everything after tests it. "
        "This is the correct way to validate financial ML models."
    )

    st.warning(
        "**GARCH outputs as LSTM features — not raw prices.**\n\n"
        "Raw oil prices are non-stationary and nearly "
        "impossible to predict directly. GARCH conditional "
        "volatility is stationary, mean-reverting, and has "
        "economic meaning. Using it as input gives the LSTM "
        "a fighting chance to learn real patterns."
    )

    st.markdown("---")

    # TECH STACK
    st.subheader("Tech Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**Data & Modelling**\n\n"
            "Python · Pandas · NumPy\n"
            "arch (GARCH fitting)\n"
            "TensorFlow / Keras (LSTM)\n"
            "scikit-learn (scaling)"
        )

    with col2:
        st.info(
            "**Dashboard**\n\n"
            "Streamlit\n"
            "Plotly (interactive charts)\n"
            "Deployed on Streamlit Cloud"
        )

    with col3:
        st.info(
            "**Data Source**\n\n"
            "BRENT Crude Oil — Yahoo Finance\n"
            "NSE Stock Prices — Yahoo Finance\n"
            "Period: Jul 2007 – Dec 2024"
        )

    st.markdown("---")

    # HONEST ASSESSMENT
    st.subheader("Honest Model Assessment")

    st.error(
        "**53% directional accuracy is modest.**\n\n"
        "Markets are nearly efficient. Predicting direction "
        "consistently above 55% over 2 years of test data "
        "would be extraordinary. We do not overclaim.\n\n"
        "The real value of OilPulse is not raw prediction "
        "accuracy — it is regime-aware stock positioning. "
        "Knowing the market is in CRISIS regime changes "
        "which stocks you watch, even without a precise "
        "price forecast. That is the actionable insight."
    )