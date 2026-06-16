# core/styles.py
import streamlit as st

def apply_terminal_theme():
    """Streamlit-এর লেটেস্ট ইঞ্জিনের জন্য আল্ট্রা-স্টাইলিশ ও বড় সাইডবার মেনু বাটন"""
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

        /* =========================================================================
           🚀 নতুন স্ট্রিমলিট ইঞ্জিনের জন্য মোবাইল ফ্রেন্ডলি গ্লোয়িং মেনু বাটন (Fixed)
           ========================================================================= */
        /* প্রতিটা রেডিও অপশনের কন্টেইনার গ্যাপ বাড়ানো */
        [data-testid="stSidebar"] div[data-testid="stRadio"] {
            padding-top: 15px;
        }
        
        [data-testid="stSidebar"] div[data-testid="stRadio"] > div {
            gap: 16px !important;
        }

        /* প্রতিটা মেনু বাটনকে বড় ৩ডি ব্লকে রূপান্তর */
        [data-testid="stSidebar"] div[data-testid="stRadio"] [data-testid="stWidgetLabel"] {
            background-color: #121829 !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            border: 1px solid #1e294b !important;
            color: #a0aec0 !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            display: block !important;
            width: 100% !important;
            min-height: 55px !important;
            line-height: 23px !important;
            transition: all 0.25s ease-in-out !important;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3) !important;
            cursor: pointer !important;
            text-align: left !important;
        }

        /* ডিফল্ট গোল রেডিও সার্কেল এবং ছোট টেক্সট হাইড করার অফিশিয়াল ট্রিক */
        [data-testid="stSidebar"] div[data-testid="stRadio"] label div:first-child {
            display: none !important;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] label {
            display: block !important;
            width: 100% !important;
            padding: 0px !important;
            margin: 0px !important;
        }

        /* মোবাইলে টাচ বা হোভার এফেক্ট */
        [data-testid="stSidebar"] div[data-testid="stRadio"] [data-testid="stWidgetLabel"]:hover {
            border-color: #00e5ff !important;
            color: #00e5ff !important;
            background-color: #16223f !important;
            box-shadow: 0px 0px 12px rgba(0, 229, 255, 0.2) !important;
            transform: translateY(-2px);
        }

        /* 🟢 একটিভ/সিলেক্টেড মেনু বাটনের রাজকীয় নিয়ন গ্রিন গ্লো এফেক্ট */
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > div:has(input:checked) [data-testid="stWidgetLabel"] {
            background: linear-gradient(135deg, #142834 0%, #0d2e27 100%) !important;
            border: 2px solid #00e676 !important;
            color: #00e676 !important;
            box-shadow: 0px 0px 18px rgba(0, 230, 118, 0.4) !important;
            font-weight: 800 !important;
            text-shadow: 0 0 5px rgba(0, 230, 118, 0.3);
        }
        /* ========================================================================= */

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
    st.markdown("""
        <div class="header-banner">
            <div class="header-title">🟢 GREEN BULL RIDER</div>
            <div class="header-subtitle">🚀 Creator & Fund Manager — Biswajit Jana</div>
        </div>
    """, unsafe_allow_html=True)

def render_terminal_footer():
    st.markdown("""
        <div class="footer-terminal">
            📊 Alpha Terminal Core v4.0 | Fully Modular Architecture | Engineered for <b>Green Bull Rider</b> (Biswajit Jana)
        </div>
    """, unsafe_allow_html=True)
