# core/styles.py
import streamlit as st

def apply_terminal_theme():
    st.set_page_config(page_title="Alpha Moat Engine v9.0", page_icon="🦅", layout="wide")
    
    # Custom CSS Injector for Terminal View
    st.markdown("""
        <style>
        .stApp {
            background-color: #0d0f12;
            color: #e2e8f0;
            font-family: 'Courier New', Courier, monospace;
        }
        h1, h2, h3, h4 {
            color: #00ffcc !important;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
        }
        .stButton>button {
            background-color: #1a1f26;
            color: #00ffcc;
            border: 1px solid #00ffcc;
            border-radius: 4px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00ffcc;
            color: #0d0f12;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #1e293b;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    st.markdown("# 🦅 ALPHA MOAT QUANT TERMINAL v9.0")
    st.markdown("`⚡ SECURE BATCH ENGINE` | `🔒 BYPASS MODE ACTIVE` | `🛰️ DATA ROUTE: YAHOO REPLICA`")
    st.markdown("---")

def render_terminal_footer():
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b;'>🔒 End of Secure Terminal Session | Designed for High-Alpha Compliant Operations</p>", unsafe_allow_html=True)
