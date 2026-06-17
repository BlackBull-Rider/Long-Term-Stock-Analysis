# core/styles.py
import streamlit as st

def apply_terminal_theme():
    st.set_page_config(page_title="GREEN BULL RIDER | METRICS LAYER", page_icon="⚡", layout="wide")
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=400;700;900&family=Share+Tech+Mono&display=swap');
        
        .stApp {
            background: radial-gradient(circle at 50% 50%, #070b12 0%, #020406 100%) !important;
            color: #c3d1e0 !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        
        .hud-banner {
            background: linear-gradient(135deg, rgba(0, 255, 170, 0.04) 0%, rgba(0, 191, 255, 0.01) 100%);
            padding: 18px;
            border-radius: 8px;
            border: 1px solid rgba(0, 255, 170, 0.2);
            box-shadow: 0px 0px 25px rgba(0, 255, 170, 0.05);
            margin-bottom: 20px;
            text-align: center;
        }
        .hud-title {
            font-family: 'Orbitron', sans-serif;
            color: #00ffaa !important;
            font-size: 32px !important;
            font-weight: 900 !important;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(0, 255, 170, 0.4);
        }
        .hud-subtitle {
            color: #00bfff !important;
            font-size: 12px !important;
            letter-spacing: 2px;
            margin-top: 5px;
        }

        .stButton>button {
            background: linear-gradient(180deg, #111a24 0%, #06090d 100%) !important;
            color: #00ffaa !important;
            border: 1px solid rgba(0, 255, 170, 0.25) !important;
            font-family: 'Orbitron', sans-serif !important;
            padding: 10px 20px !important;
            font-weight: 700 !important;
            width: 100% !important;
            border-radius: 4px !important;
        }
        .stButton>button:hover {
            color: #020406 !important;
            background: #00ffaa !important;
            box-shadow: 0 0 20px rgba(0, 255, 170, 0.5) !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(0, 255, 170, 0.12) !important;
            background-color: rgba(5, 9, 16, 0.85) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    st.markdown("""
        <div class="hud-banner">
            <div class="hud-title">⚡ GREEN BULL RIDER ⚡</div>
            <div class="hud-subtitle">🤖 PRO QUANT DATA LAYER ENGINE // OPERATOR: BISWAJIT JANA</div>
        </div>
    """, unsafe_allow_html=True)

def render_operational_guidelines():
    st.markdown("""
    <div style="background: rgba(6, 11, 20, 0.9); border-left: 4px solid #00bfff; padding: 12px; margin-top: 20px; font-size: 13px; border: 1px solid rgba(0, 191, 255, 0.1);">
        <strong style="color:#00bfff;">📡 QUANT STRATEGY COMPLIANCE LAYER:</strong><br/>
        • Strict multi-threaded parallel array mapping engine loading live listed assets.<br/>
        • Repository data files are mirrored directly into secure cloud states to avoid application memory crashes.
    </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #475569; font-size: 11px;'>🔒 master architecture secured // 5000+ stock matrix pipeline online</p>", unsafe_allow_html=True)
