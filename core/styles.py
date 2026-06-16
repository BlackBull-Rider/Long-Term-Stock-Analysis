# core/styles.py
import streamlit as st

def apply_terminal_theme():
    st.markdown("""
        <style>
        .stApp { background-color: #070913; color: #d1d7e0; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #0b0e1a; border-right: 2px solid #161f38; }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] { gap: 12px !important; padding-top: 10px; }
        [data-testid="stSidebar"] div[data-testid="stRadio"] label {
            background-color: #121829 !important; border: 1px solid #1e294b !important; border-radius: 8px !important;
            padding: 14px 16px !important; min-height: 52px !important; width: 100% !important;
            transition: all 0.2s ease-in-out !important; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2) !important; margin: 0px !important;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] label p { font-size: 16px !important; font-weight: 700 !important; color: #cbd5e1 !important; }
        [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover { border-color: #00e5ff !important; background-color: #16223f !important; }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > div:has(input:checked) label {
            background: linear-gradient(135deg, #142834 0%, #0d2e27 100%) !important;
            border: 2px solid #00e676 !important; box-shadow: 0px 0px 15px rgba(0, 230, 118, 0.3) !important;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > div:has(input:checked) label p { color: #00e676 !important; }
        h4 { color: #00e5ff !important; font-size: 18px !important; font-weight: 700 !important; margin-top: 25px !important; border-bottom: 1px solid #1e294b; padding-bottom: 8px; }
        div[data-testid="stNumberInput"] input { background-color: #121829 !important; color: #ffffff !important; border: 1px solid #1e294b !important; border-radius: 6px !important; font-weight: 600 !important; }
        div[data-testid="stDataFrame"] { background-color: #0f1424 !important; border: 1px solid #1e294b !important; border-radius: 8px !important; }
        .header-banner { background: linear-gradient(135deg, #0d1b2a 0%, #1b4332 100%); padding: 25px; border-radius: 12px; border: 2px solid #00e676; box-shadow: 0px 0px 20px rgba(0, 230, 118, 0.2); margin-bottom: 25px; text-align: center; }
        .header-title { color: #00e676 !important; font-size: 32px !important; font-weight: 800 !important; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0, 230, 118, 0.5); }
        .header-subtitle { color: #00e5ff !important; font-size: 16px !important; font-weight: 600; }
        div[data-testid="stMetric"] { background-color: #0f1424; padding: 18px; border-radius: 10px; border: 1px solid #1e294b; border-left: 5px solid #00e5ff; }
        .footer-terminal { background-color: #0b0e1a; padding: 15px; border-radius: 8px; border-top: 2px solid #00e5ff; text-align: center; margin-top: 50px; font-size: 13px; color: #7e8b9b; }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    st.markdown("""
        <div class="header-banner">
            <div class="header-title">🟢 GREEN BULL RIDER</div>
            <div class="header-subtitle">🚀 Creator & Fund Manager — Biswajit Jana</div>
        </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    st.markdown("""
        <div class="footer-terminal">
            📊 Alpha Terminal Core v8.0 | Fully Modular Architecture | Engineered for <b>Green Bull Rider</b> (Biswajit Jana)
        </div>
    """, unsafe_allow_html=True)
