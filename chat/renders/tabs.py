import streamlit as st
import pandas as pd

from renders.text import render_text
from renders.table import render_table

def render_tabs(dados):

    st.markdown("""
    <style>
    /* container das tabs */
    div[data-testid="stTabs"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* botão das tabs */
    button[data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 500;
        padding: 8px 16px;
        color: #6b7280;
        border-radius: 8px;
    }

    /* tab ativa */
    button[aria-selected="true"] {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
        font-weight: 600;
    }

    /* hover */
    button[data-baseweb="tab"]:hover {
        background-color: #f9fafb;
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([
        " Resumo",
        " Tabela"
    ])

    with tab1:
        render_text(dados)
 

    with tab2:
        render_table(dados)