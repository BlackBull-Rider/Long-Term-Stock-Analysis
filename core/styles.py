# core/styles.py
import streamlit as st

def apply_terminal_theme():
    st.set_page_config(page_title="GREEN BULL RIDER | QUANT HFT v10.0", page_icon="⚡", layout="wide")
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
        
        .stApp {
            background: radial-gradient(circle at 50% 50%, #0a0e17 0%, #04060a 100%);
            color: #c3d1e0;
            font-family: 'Share Tech Mono', monospace;
        }
        
        /* 🌌 Futuristic Glowing Banner HUD */
        .hud-banner {
            background: linear-gradient(135deg, rgba(0, 255, 204, 0.05) 0%, rgba(0, 229, 255, 0.02) 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 204, 0.3);
            box-shadow: 0px 0px 25px rgba(0, 255, 204, 0.1), inset 0 0 15px rgba(0, 255, 204, 0.05);
            margin-bottom: 30px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .hud-title {
            font-family: 'Orbitron', sans-serif;
            color: #00ffcc !important;
            font-size: 32px !important;
            font-weight: 900 !important;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(0, 255, 204, 0.6);
            margin-bottom: 2px;
        }
        .hud-subtitle {
            font-family: 'Share Tech Mono', monospace;
            color: #00e5ff !important;
            font-size: 14px !important;
            letter-spacing: 2px;
            text-transform: uppercase;
            opacity: 0.8;
        }

        /* 💾 Glassmorphic Card Engine for Metrics */
        .quant-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-top: 3px solid #00ffcc;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(5px);
            margin-bottom: 15px;
        }
        .quant-card-loss {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-top: 3px solid #ff3366;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(5px);
            margin-bottom: 15px;
        }
        
        .quant-val {
            font-family: 'Orbitron', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            text-shadow: 0 0 10px rgba(255,255,255,0.1);
        }

        /* 🔘 Tactile Neon Buttons */
        .stButton>button {
            background: linear-gradient(180deg, #16222f 0%, #0d151d 100%) !important;
            color: #00ffcc !important;
            border: 1px solid rgba(0, 255, 204, 0.4) !important;
            border-radius: 4px !important;
            font-family: 'Orbitron', sans-serif !important;
            font-size: 14px !important;
            letter-spacing: 2px !important;
            padding: 12px 30px !important;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }
        .stButton>button:hover {
            color: #0d0f12 !important;
            background: #00ffcc !important;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.7) !important;
            border: 1px solid #00ffcc !important;
        }

        /* 📊 Institutional Data Grid Overlay */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(0, 255, 204, 0.15);
            background-color: rgba(10, 15, 26, 0.7);
            border-radius: 8px;
            padding: 5px;
        }

        .guide-box {
            background: rgba(13, 22, 38, 0.8);
            border-left: 4px solid #00e5ff;
            padding: 18px;
            border-radius: 6px;
            margin-top: 35px;
            font-size: 13px;
            border: 1px solid rgba(0, 229, 255, 0.1);
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.02);
        }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    st.markdown("""
        <div class="hud-banner">
            <div class="hud-title">⚡ GREEN BULL RIDER ⚡</div>
            <div class="hud-subtitle">🤖 PRO QUANT INSTITUTIONAL TERMINAL v10.0 // OPERATOR: BISWAJIT JANA</div>
        </div>
    """, unsafe_allow_html=True)

def render_operational_guidelines():
    st.markdown("""
    <div class="guide-box">
        <span style="color:#00e5ff; font-weight:bold; font-family:'Orbitron', sans-serif;">📡 QUANT COMPLIANCE & VECTOR EXECUTION ENGINE PROTOCOLS:</span><br/><br/>
        • <strong>MULTI-YEAR RADAR:</strong> Systems mapping asset metrics crunch up to 7-years historical weekly candle structures to locate micro-consolidation loops.<br/>
        • <strong>MOAT ALPHA VECTOR:</strong> Gross Margin tracking identifies defensive monopolies. If baseline margin structures compromise, alpha decay triggers.<br/>
        • <strong>RISK MITIGATION SPREAD:</strong> Distance vectors calculated from the 200-period Exponential Moving Average control execution sizing models.<br/>
        • <strong>ISOLATED COMPUTATION LAYER:</strong> Local host sandbox architecture ensures localized cache synchronization. System integrity remains absolute.
    </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #475569; font-size: 11px; letter-spacing: 1px;'>🔒 MASTER CORE ONLINE // ZERO TRACK FOOTPRINT OPERATIONAL COMPLIANT</p>", unsafe_allow_html=True)
