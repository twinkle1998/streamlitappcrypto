# ============================================================
# Twinkle — Ethereum (ETH) Forecasting Dashboard
# Final Stable Version — Local Cache + Retry + Fallback Fix
# ============================================================

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import time, threading, random, json
from functools import lru_cache

# ----------------------------
# Constants
# ----------------------------
COINGECKO = "https://api.coingecko.com/api/v3"
COIN_ID = "ethereum"
FASTAPI = "https://fastapiethereum.onrender.com"

# ----------------------------
# Theme Injection
# ----------------------------
def _inject_theme():
    st.markdown("""
    <style>
    :root {
      --bg: #0B0E11;
      --panel: #0E1116;
      --border: #1F2937;
      --text: #E5E7EB;
      --muted: #9CA3AF;
      --gold: #F0B90B;
    }
    html, body, [class*="css"] {
      background-color: var(--bg) !important;
      color: var(--text) !important;
      font-family: 'Inter', system-ui, sans-serif !important;
    }
    h1, h2, h3, h4 { color: var(--text) !important; font-weight: 600; }
    a { color: var(--gold) !important; text-decoration: none; }
    .kpi {
      background: #111318;
      border: 1px solid rgba(240,185,11,0.25);
      border-radius: 14px;
      padding: 18px;
      text-align: center;
    }
    .kpi h3 {
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 4px;
    }
    .kpi p {
      color: var(--text);
      font-weight: 700;
      font-size: 1.4rem;
      margin: 0;
    }
    .divider {
      height: 1px;
      background: var(--border);
      margin: 2rem 0;
    }
    .heading-yellow {
      color: var(--gold);
      font-size: 1.8rem;
      font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)


# ----------------------------
# Helper — Safe Caching Hash
# ----------------------------
def _make_hashable(params):
    """Convert dict to hashable string for caching"""
    if params is None:
        return None
    return json.dumps(params, sort_keys=True)


# ----------------------------
# Helper — API Fetch (Retry + Cache + Fallback)
# ----------------------------
@lru_cache(maxsize=16)
def _fetch(url, params_hash=None, retries=3, delay=2):
    """Fetch JSON with retry, local memory cache, and fallback"""
    params = json.loads(params_hash) if params_hash else None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception:
            if attempt < retries - 1:
                time.sleep(delay + random.uniform(0.3, 1.0))
            else:
                st.warning("⚠️ API is responding slowly — showing cached or sample data if available.")
                try:
                    if "market_chart" in url:
                        return pd.read_json("backup_market_chart.json").to_dict(orient="records")
                    elif "ohlc" in url:
                        return pd.read_json("backup_ohlc.json").to_dict(orient="records")
                except:
                    return None


# ----------------------------
# Cached API Endpoints
# ----------------------------
@st.cache_data(ttl=600)
def get_metadata():
    return _fetch(f"{COINGECKO}/coins/{COIN_ID}")

@st.cache_data(ttl=300)
def get_live_market():
    params = {
        "ids": COIN_ID,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    return _fetch(f"{COINGECKO}/simple/price", _make_hashable(params))

@st.cache_data(ttl=600)
def get_ohlc(days=90):
    params = {"vs_currency": "usd", "days": days}
    return _fetch(f"{COINGECKO}/coins/{COIN_ID}/ohlc", _make_hashable(params))

@st.cache_data(ttl=600)
def get_market_chart(days=90):
    params = {"vs_currency": "usd", "days": days}
    return _fetch(f"{COINGECKO}/coins/{COIN_ID}/market_chart", _make_hashable(params))


# ----------------------------
# Visualization Builders
# ----------------------------
def plot_candlestick(ohlc):
    if not ohlc:
        return None
    df = pd.DataFrame(ohlc, columns=["ts", "open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df["ts"], unit="ms")
    fig = go.Figure(data=[go.Candlestick(
        x=df["date"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name="ETH"
    )])
    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB",
        xaxis_title="Date", yaxis_title="Price (USD)"
    )
    return fig


def plot_line(series, label, height=280):
    if not series:
        return None
    df = pd.DataFrame(series, columns=["ts", "value"])
    df["date"] = pd.to_datetime(df["ts"], unit="ms")
    fig = px.line(df, x="date", y="value", labels={"value": label})
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E5E7EB"
    )
    return fig


# ----------------------------
# Background Warm-Up
# ----------------------------
def _warm_coingecko():
    """Light background warm-up to reduce initial lag"""
    try:
        get_live_market()
        get_ohlc(30)
        get_metadata()
    except:
        pass


# ----------------------------
# Main App
# ----------------------------
def app():
    _inject_theme()
    threading.Thread(target=_warm_coingecko, daemon=True).start()

    st.markdown("<h1 class='heading-yellow'>Ethereum Next-Day High Price Prediction</h1>", unsafe_allow_html=True)
    st.caption("Powered by CoinGecko & FastAPI · AT3 Group 1, UTS 2025")
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 1 — Prediction via FastAPI
    # ============================================================
    today = date.today()
    iframe_url = f"{FASTAPI}/predict/ethereum?date={today.isoformat()}"
    components.iframe(iframe_url, height=520, scrolling=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 2 — Market Overview KPIs
    # ============================================================
    st.markdown("### Live Market Snapshot")
    with st.spinner("Loading live market data..."):
        mk = get_live_market()
    if mk and COIN_ID in mk:
        data = mk[COIN_ID]
        colA, colB, colC, colD = st.columns(4)
        metrics = [
            ("Price (USD)", f"${data.get('usd', 0):,.2f}"),
            ("24h Change (%)", f"{data.get('usd_24h_change', 0):,.2f}%"),
            ("Market Cap (USD)", f"${data.get('usd_market_cap', 0):,.0f}"),
            ("24h Volume (USD)", f"${data.get('usd_24h_vol', 0):,.0f}")
        ]
        for i, (label, value) in enumerate(metrics):
            with [colA, colB, colC, colD][i]:
                st.markdown(f"<div class='kpi'><h3>{label}</h3><p>{value}</p></div>", unsafe_allow_html=True)
    else:
        st.info("Data temporarily unavailable — please retry later.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 3 — Historical Charts
    # ============================================================
    st.markdown("### Historical Market Performance")
    with st.spinner("Fetching historical charts..."):
        days = 90
        ohlc = get_ohlc(days)
        market_chart = get_market_chart(days)

    fig_candle = plot_candlestick(ohlc)
    if fig_candle:
        st.plotly_chart(fig_candle, use_container_width=True)
    else:
        st.info("Price history unavailable right now.")

    if market_chart:
        for key, label in [("market_caps", "Market Cap (USD)"), ("total_volumes", "Trading Volume (USD)")]:
            if market_chart.get(key):
                fig = plot_line(market_chart[key], label)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 4 — Project Fundamentals
    # ============================================================
    st.markdown("### Ethereum Fundamentals")
    with st.spinner("Loading Ethereum fundamentals..."):
        meta = get_metadata()
    if meta:
        logo = meta["image"]["large"]
        st.markdown(f"<img src='{logo}' width='80'>", unsafe_allow_html=True)
        st.markdown(f"**Name:** {meta['name']}  |  **Symbol:** {meta['symbol'].upper()}")
        st.markdown(f"**Algorithm:** {meta.get('hashing_algorithm','N/A')}")
        st.markdown(f"**Category:** {', '.join(meta.get('categories', []))}")
        st.markdown(f"[Website]({meta['links']['homepage'][0]}) | [Explorer]({meta['links']['blockchain_site'][0]})")
    else:
        st.info("Project fundamentals unavailable — please refresh later.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ============================================================
    # SECTION 5 — Summary
    # ============================================================
    st.markdown("### Summary")
    st.markdown("""
    This dashboard delivers:
    - Real-time Ethereum market data via CoinGecko (locally cached)
    - Interactive candlestick and historical charts
    - Next-day high price prediction via FastAPI ML model
    - Auto-retry + fallback for stable performance
    """)
    st.caption("Developed by Twinkle · AT3 Group 1 · University of Technology Sydney (2025)")

# Run App
if __name__ == "__main__":
    app()
