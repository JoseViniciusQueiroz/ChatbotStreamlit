import streamlit as st
import pandas as pd

def render_table(dados):
    if not isinstance(dados, list):
        st.error("Formato inválido.")
        st.write(dados)
        return

    df = pd.DataFrame(dados)
    df = df.drop(columns=["id"], errors="ignore")

    html = """
    <style>
        .table-container {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
            background-color: #ffffff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }

        thead {
            background-color: #f3f4f6;
        }

        th {
            text-align: left;
            padding: 12px;
            color: #111827;
            font-size: 14px;
            border-bottom: 1px solid #e5e7eb;
        }

        td {
            padding: 12px;
            color: #374151;
            font-size: 14px;
            border-bottom: 1px solid #f1f1f1;
        }

        tr:hover {
            background-color: #f9fafb;
        }

        tr:last-child td {
            border-bottom: none;
        }
    </style>
    """

    html += '<div class="table-container"><table>'

    html += "<thead><tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead>"
    html += "<tbody>"
    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"

    st.markdown(html, unsafe_allow_html=True)