# core/styles.py
import streamlit as st

def apply_terminal_theme():
    """পুরো অ্যাপ্লিকেশনের জন্য নিয়ন সাইবার-ডার্ক সিএসএস থিম"""
    st.markdown("""
        <style>
        /* মেইন রেসপনসিভ ব্যাকগ্রাউন্ড */
        .stApp {
            background-color: #070913;
            color: #d1d7e0;
            font-family: 'Inter', sans-serif;
        }
        /* সাইডবার প্যানেল ডিজাইন */
        [data-testid="stSidebar"] {
            background-color: #0b0e1a;
            border-right: 2px solid #161f38;
        }
        /* গ্লোয়িং প্রফেশনাল ফান্ড ম্যানেজার হেডার ব্যানার */
        .header-banner {
            background: linear-gradient(135deg, #0d1b2a 0%, #1b4332 100%);
            padding: 25px;
            border-radius: 12px;
            border: 2px solid #00e676;
            box-shadow: 0px 0px 20px rgba(0, 230, 118, 0.2);
            margin-bottom: 25px;
            text-align: center;
        }
        .header-title {
            color: #00e676 !important;
            font-size: 32px !important;
            font-weight: 800 !important;
            letter-spacing: 2px;
            margin-bottom: 5px;
            text-shadow: 0 0 10px rgba(0, 230, 118, 0.5);
        }
        .header-subtitle {
            color: #00e5ff !important;
            font-size: 16px !important;
            font-weight: 600;
            letter-spacing: 1px;
        }
        /* হোভার এফেক্ট সহ ৩ডি মেট্রিক কার্ড */
        div[data-testid="stMetric"] {
            background-color: #0f1424;
            padding: 18px;
            border-radius: 10px;
            border: 1px solid #1e294b;
            border-left: 5px solid #00e5ff;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.5);
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #00e676;
            box-shadow: 0px 0px 15px rgba(0, 230, 118, 0.3);
        }
        /* ঝাক্কাস টার্মিনাল ফুটার */
        .footer-terminal {
            background-color: #0b0e1a;
            padding: 15px;
            border-radius: 8px;
            border-top: 2px solid #00e5ff;
            text-align: center;
            margin-top: 50px;
            font-size: 13px;
            color: #7e8b9b;
        }
        </style>
    """, unsafe_allow_html=True)

def render_branding_header():
    """প্রধান ব্র্যান্ডিং প্যানেল"""
    st.markdown("""
        <div class="header-banner">
            <div class="header-title">🟢 GREEN BULL RIDER</div>
            <div class="header-subtitle">🚀 Creator & Fund Manager — Biswajit Jana</div>
        </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    """ব্র্যান্ডেড প্রফেশনাল ফুটার সিগনেচার"""
    st.markdown("""
        <div class="footer-terminal">
            📊 Alpha Terminal Core v4.0 | Fully Modular Architecture | Engineered for <b>Green Bull Rider</b> (Biswajit Jana)
        </div>
    """, unsafe_allow_html=True)
