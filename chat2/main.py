"""
Chat AI com Function Calling, Logging e Observabilidade
Dashboard com métricas de performance, custos e execução
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import defaultdict

from agent import AIAgent
from logger import logger
from functions import registry


# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Chat AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CSS
# ============================================================================

st.markdown("""
<style>
:root {
    --primary: #5a5a5a;
    --primary-light: #8a8a8a;
    --primary-lighter: #b0b0b0;
    --bg-main: #fafafa;
    --bg-card: #ffffff;
    --bg-hover: #f5f5f5;
    --border: #e8e8e8;
    --text-primary: #2d2d2d;
    --text-secondary: #666666;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-main);
}

.chat-message {
    padding: 14px;
    border-radius: 12px;
    margin: 8px 0;
}

.chat-message.user {
    background: var(--bg-hover);
    margin-left: 15%;
    border-left: 3px solid var(--primary-lighter);
}

.chat-message.assistant {
    background: var(--bg-card);
    margin-right: 15%;
    border: 1px solid var(--border);
}

</style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE
# ============================================================================

if "agent" not in st.session_state:
    st.session_state.agent = AIAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "execution_metrics" not in st.session_state:
    st.session_state.execution_metrics = []


# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<h1>💬 Chat AI</h1>
<p>Function Calling + Logs + Observabilidade</p>
""", unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Controles")

    if st.button("🔄 Limpar Chat"):
        st.session_state.messages = []
        st.session_state.execution_metrics = []
        st.toast("Chat limpo")

    if st.button("🗑️ Limpar Logs"):
        logger.clear_logs()
        st.toast("Logs limpos")

    st.divider()

    stats = logger.get_stats()

    st.markdown("### 📊 Métricas")
    st.metric("Execuções", stats["total_function_calls"])
    st.metric("Mensagens", stats["total_messages"])
    st.metric("Logs", stats["total_logs"])
    st.metric("Erros", stats["errors"])


# ============================================================================
# TABS
# ============================================================================

tab_chat, tab_logs, tab_charts, tab_docs = st.tabs(
    ["💬 Chat", "📋 Logs", "📈 Charts", "📖 Docs"]
)


# ============================================================================
# TAB CHAT
# ============================================================================

with tab_chat:

    st.markdown("### Conversa")

    for message in st.session_state.messages:
        css = "user" if message["role"] == "user" else "assistant"
        label = "Você" if message["role"] == "user" else "Agent"

        st.markdown(f"""
        <div class="chat-message {css}">
            <b>{label}</b><br>{message["content"]}
        </div>
        """, unsafe_allow_html=True)

    user_input = st.text_input("Mensagem")

    if st.button("Enviar") and user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        import time
        start = time.time()

        response, metadata = st.session_state.agent.process_message(user_input)

        exec_time = (time.time() - start) * 1000

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.execution_metrics.append({
            "input": user_input,
            "exec_time": exec_time,
            "timestamp": datetime.now().isoformat()
        })

        st.rerun()


# ============================================================================
# TAB LOGS
# ============================================================================

with tab_logs:

    st.markdown("### Logs")

    logs = logger.get_all_logs()

    if logs:
        st.dataframe(pd.DataFrame(logs), use_container_width=True)
    else:
        st.info("Nenhum log ainda")


# ============================================================================
# TAB CHARTS
# ============================================================================

with tab_charts:

    st.markdown("### Performance")

    func_logs = logger.get_function_logs()

    if func_logs:

        times = [l.get("execution_time_ms", 0) for l in func_logs]

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=times, mode="lines+markers"))

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Sem dados")


# ============================================================================
# TAB DOCS (RESTAURADA)
# ============================================================================

with tab_docs:

    st.markdown("### 📖 Documentação")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        **Objetivo**

        Este projeto demonstra:
        - Chat com IA simulada
        - Function calling
        - Logging estruturado
        - Observabilidade
        """)

        st.markdown("---")

        st.markdown("""
        **Fluxo**

        1. Usuário envia mensagem  
        2. IA detecta intenção  
        3. Executa função  
        4. Registra logs  
        5. Retorna resposta  
        """)

    with col2:

        st.markdown("""
        **Funções disponíveis**

        - Multiplicar números  
        - Arredondar valores  
        - Saudação personalizada  
        """)

    st.divider()

    with st.expander("🔍 Arquitetura"):
        st.markdown("""
        Input → Agent → Intent → Function → Logger → UI
        """)

    with st.expander("📚 Estrutura do projeto"):
        st.markdown("""
        - agent.py  
        - logger.py  
        - functions.py  
        - main.py (Streamlit UI)
        """)


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.markdown("""
<div style="text-align:center;color:#999;">
Chat AI v1.0 • Streamlit
</div>
""", unsafe_allow_html=True)