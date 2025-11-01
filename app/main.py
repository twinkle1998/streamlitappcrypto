# ============================================================
# AT3 — Streamlit Frontend for Cryptocurrency Forecast Portal
# ============================================================

import streamlit as st
import importlib
import sys, os
from urllib.parse import urlencode

# ============================================================
# --- PATH SETUP (Fixed for student imports)
# ============================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
STUDENTS_PATH = os.path.join(ROOT_DIR, "students")

if STUDENTS_PATH not in sys.path:
    sys.path.append(STUDENTS_PATH)

# ============================================================
# --- PAGE CONFIG ---
# ============================================================
st.set_page_config(page_title="AT3 — Crypto Forecast Portal", layout="wide")

# ============================================================
# --- DYNAMIC MODULE LOADER ---
# ============================================================
def load_student_page(student_name: str):
    """Dynamically loads and executes a student's Streamlit tab."""
    try:
        module = importlib.import_module(f"{student_name}")
        if hasattr(module, "show_ethereum_tab"):
            module.show_ethereum_tab()
        elif hasattr(module, "app"):
            module.app()
        else:
            st.error(f"⚠️ Module '{student_name}' found but has no callable entry function.")
    except Exception as e:
        st.error(f"❌ Unable to load {student_name}'s module.\n\n{e}")

# ============================================================
# --- CUSTOM CSS ---
# ============================================================
st.markdown(
    """
    <style>
    :root {
      --gold:#D4AF37;
      --gold-dark:#caa63d;
      --text:#ffffff;
      --muted:#bcbcbc;
    }

    html, body, .stApp {
      height: 100vh !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow-x: hidden !important;
      color: var(--text);
      font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-image: url("https://i.postimg.cc/52qrXgZH/pexels-alesiakozik-6770611.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        position: relative;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.70);
        z-index: 0;
    }

    .hero, .token-bar, .team {
      position: relative;
      z-index: 1;
    }

    .hero {
      text-align: center;
      padding: 34px 20px 0 20px;
      height: 41vh;
    }

    .hero h1 {
      font-size: 2.3rem;
      font-weight: 800;
      color: var(--gold);
      text-shadow: 0 0 12px rgba(212,175,55,0.4);
      margin-bottom: 8px;
    }

    .hero p {
      color: var(--gold-dark);
      font-size: 1.05rem;
      margin-bottom: 8px;
    }

    .hero-desc {
      color: var(--muted);
      max-width: 760px;
      margin: 0 auto 6px auto;
      font-size: 0.95rem;
      line-height: 1.5;
    }

    .hero a.learn-btn {
      background: var(--gold);
      color: black !important;
      text-decoration: none;
      padding: 10px 24px;
      font-weight: 700;
      border-radius: 6px;
      transition: 0.3s ease;
      display: inline-block;
      box-shadow: 0 0 10px rgba(212,175,55,0.3);
      margin-top: 6px;
      margin-bottom: 16px;
    }

    .hero a.learn-btn:hover {
      background: #e0c157;
      box-shadow: 0 0 18px rgba(212,175,55,0.5);
    }

    .hero small {
      display: block;
      color: var(--gold-dark);
      margin-top: 70px;
      font-weight: 700;
      letter-spacing: 1px;
      font-size: 1.2rem;
      text-transform: uppercase;
      text-shadow: 0 0 8px rgba(212,175,55,0.4);
    }

    .token-bar {
      background: rgba(17,17,17,0.88);
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      height: 19vh;
      border-top: 1px solid #1c1c1c;
      border-bottom: 1px solid #1c1c1c;
      padding: 2px 3%;
    }

    .token {
      flex: 1 1 20%;
      text-align: center;
      padding: 8px 6px;
      border-radius: 10px;
      transition: all 0.3s ease;
      max-width: 280px;
      cursor: pointer;
      text-decoration: none;
    }

    .token:hover {
      background: rgba(212,175,55,0.08);
      box-shadow: 0 0 16px rgba(212,175,55,0.25);
    }

    .token h3 {
      color: var(--gold);
      font-size: 1rem;
      margin-bottom: 3px;
    }

    .token p {
      color: var(--muted);
      font-size: 0.84rem;
      line-height: 1.3;
      margin: 0;
    }

    .team {
      background: rgba(10,10,10,0.92);
      text-align: center;
      height: 30vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      border-top: 1px solid #1a1a1a;
      overflow: hidden;
      padding: 5px 0;
    }

    .team h3 {
      color: var(--gold);
      margin-bottom: 5px;
    }

    .member-container {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      padding: 0 3%;
    }

    .member {
      flex: 1 1 20%;
      text-align: center;
      padding: 3px;
      max-width: 250px;
    }

    .member-img {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
      border: 2px solid rgba(212,175,55,0.6);
      margin: 0 auto 3px auto;
    }

    .member p {
      color: var(--muted);
      font-size: 0.82rem;
      margin: 0;
      line-height: 1.3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# --- URL PARAM HANDLING ---
# ============================================================
query_params = st.query_params
active_student = query_params.get("student")
if isinstance(active_student, list):
    active_student = active_student[0]

# ============================================================
# --- CONDITIONAL PAGE RENDERING ---
# ============================================================
if active_student:
    load_student_page(active_student)
else:
    # === LANDING PAGE ===
    st.markdown(
        """
        <div class="hero">
          <h1>SECURE AND INTELLIGENT WAY TO FORECAST CRYPTOCURRENCY</h1>
          <p>Machine Learning–Driven Forecasts for ETH, SOL, XRP, and BTC.</p>

          <div class="hero-desc">
            Our project integrates advanced machine-learning models to predict cryptocurrency trends with precision.
            By leveraging real-time APIs and optimized XGBoost algorithms, we aim to make digital-asset forecasting
            accessible, transparent, and data-driven for educational and analytical use.
          </div>

          <a href="https://coinmarketcap.com/alexandria/" target="_blank" class="learn-btn">LEARN MORE</a>
          <small>Explore Tokens</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    base_url = "?"
    st.markdown(
        f"""
        <div class="token-bar">
          <a href="{base_url + urlencode({'student':'student_twinkle'})}" target="_self" class="token">
            <h3>Ethereum (ETH)</h3>
            <p>Ethereum forecasting using an Optuna-tuned XGBoost model with live FastAPI integration.</p>
          </a>
          <a href="{base_url + urlencode({'student':'student_nidhi'})}" target="_self" class="token">
            <h3>Solana (SOL)</h3>
            <p>Feature-engineered forecasting model for trend stability and pattern recognition.</p>
          </a>
          <a href="{base_url + urlencode({'student':'student_rohan'})}" target="_self" class="token">
            <h3>XRP (XRP)</h3>
            <p>FastAPI-powered endpoint with real-time API integration and validation pipeline.</p>
          </a>
          <a href="{base_url + urlencode({'student':'student_paul'})}" target="_self" class="token">
            <h3>Bitcoin (BTC)</h3>
            <p>Predict next-day highs using optimized ML regression models for consistent accuracy.</p>
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- TEAM SECTION ---
    st.markdown(
        """
        <div class="team">
          <h3>Our Team</h3>
          <div class="member-container">
            <div class="member">
              <div class="member-img"></div>
              <p><b>Twinkle</b></p>
              <p>Developed and deployed an Optuna-tuned XGBoost model for Ethereum forecasting, integrated via FastAPI and Streamlit.</p>
            </div>
            <div class="member">
              <div class="member-img"></div>
              <p><b>Nidhi</b></p>
              <p>Solana Integration and Visualization</p>
            </div>
            <div class="member">
              <div class="member-img"></div>
              <p><b>Rohan</b></p>
              <p>XRP Deployment & Validation</p>
            </div>
            <div class="member">
              <div class="member-img"></div>
              <p><b>Paul</b></p>
              <p>Bitcoin Model & API Setup</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

