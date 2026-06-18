# app.py

import streamlit as st

from database.schema import create_tables

create_tables()

st.set_page_config(
    page_title="Green Bull Rider V6",
    layout="wide"
)

st.title(
    "🦅 Green Bull Rider V6"
)

st.success(
    "Database Initialized Successfully"
)
