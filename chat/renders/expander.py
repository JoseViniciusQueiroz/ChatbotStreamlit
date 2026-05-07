import streamlit as st
import pandas as pd

def render_expander(dados):
    df = pd.DataFrame(dados)

    st.markdown("""
    <style>
    /* container do expander */
    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        overflow: hidden;
    }

    /* cabeçalho do expander */
    div[data-testid="stExpander"] summary {
        font-size: 15px;
        font-weight: 600;
        padding: 12px;
        color: #111827;
        background-color: #f9fafb;
        border-bottom: 1px solid #e5e7eb;
        cursor: pointer;
    }

    /* hover no header */
    div[data-testid="stExpander"] summary:hover {
        background-color: #f3f4f6;
    }

    /* conteúdo interno */
    div[data-testid="stExpander"] > div {
        padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.expander("📂 Ver detalhes", expanded=False):
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )