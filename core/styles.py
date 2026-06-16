# core/styles.py
import streamlit as st

def apply_terminal_theme():
    st.set_page_config(page_title="Green Bull Rider Core v10.0", page_icon="🦅", layout="wide")
    
    st.markdown("""
        <style>
        .stApp {
            background-color: #0d0f12;
            color: #e2e8f0;
            font-family: 'Courier New', Courier, monospace;
        }
        h1, h2, h3, h4 {
            color: #00ffcc !important;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
            font-weight: 700;
        }
        .stButton>button {
            background-color: #1a1f26;
            color: #00ffcc;
            border: 1px solid #00ffcc;
            border-radius: 4px;
            font-weight: bold;
            padding: 10px 24px;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00ffcc;
            color: #0d0f12;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #1e293b;
            border-radius: 6px;
        }
        .guide-box {
            background-color: #111827;
            border-left: 4px solid #00ffcc;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            font-size: 13px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    st.markdown("# 🦅 GREEN BULL RIDER | QUANT TERMINAL v10.0")
    st.markdown("`OPERATOR: BISWAJIT JANA` | `SYSTEM STATUS: SECURE` | `DATA DEVIATION: BYPASS ACTIVE`")
    st.markdown("---")

def render_operational_guidelines():
    st.markdown("""
    <div class="guide-box">
        <strong>💡 QUANT STRATEGY OPERATIONAL ADVICE & MARKET PROTOCOLS:</strong><br/>
        • <strong>Multi-Year Breakouts:</strong> Assets crossing 5-7 years consolidation ranges carry high kinetic momentum. Accumulate strictly on volume spikes.<br/>
        • <strong>Margin Optimization:</strong> If Gross Margin drops below 35%, pricing power is diminishing. Re-evaluate structural moat positioning.<br/>
        • <strong>Risk Matrix Management:</strong> Always maintain distance rules from the 200 EMA. Avoid adding fresh exposure if the asset trades over 35% stretched from 200 EMA.<br/>
        • <strong>Compliance Safeguards:</strong> Cached system protocols guarantee localized memory computation. No live tracking footprints are generated during scanning phases.
    </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 11px;'>🔒 END OF TERMINAL SESSION | GREEN BULL RIDER FRAMEWORK</p>", unsafe_allow_html=True)
