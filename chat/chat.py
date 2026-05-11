import streamlit as st

from intents.parser import (
    identificar_intencao,
    identificar_layout
)

from core.executer import (
    executar_acao,
    renderizar_resposta
)
import time
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go

# Metrics / Logging (local `chat` package)
from logger import logger
from observability import ExecutionMetrics

st.set_page_config(page_title="Chat", layout="wide")

st.title("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tema" not in st.session_state:
    st.session_state.tema = "Claro"

# Inicializar logger/metrics (preserva comunicação com DB)
if "execution_metrics" not in st.session_state:
    st.session_state.execution_metrics = []

if "metrics" not in st.session_state:
    st.session_state.metrics = ExecutionMetrics()

if st.session_state.tema == "Escuro":

    st.markdown("""
    <style>
    body, .stApp {
        background-color: #111827 !important;
        color: #e5e7eb !important;
    }

    .block-container {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #1f2937 !important;
        border-right: 1px solid #374151;
    }

    p, span, div {
        color: #e5e7eb;
    }

    input, textarea {
        background-color: #1f2937 !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
    }

    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
    }

    div.stButton > button {
        color: #e5e7eb !important;
    }

    div.stButton > button:hover {
        color: #ffffff !important;
        transform: translateX(2px);
    }
    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>
    body, .stApp {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    .block-container {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }

    p, span, div {
        color: #111827;
    }

    input, textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #e5e7eb !important;
    }
    </style>
    """, unsafe_allow_html=True)




st.markdown("""
<style>

div[data-testid="stChatInput"] {
    background: transparent !important;
    padding: 12px 14px !important;
}

div[data-testid="stChatInput"] > div {
    background: transparent !important;
    position: relative !important;
    display: flex !important;
    align-items: center !important;
}

div[data-testid="stChatInput"] textarea {
    border-radius: 24px !important;
    border: 1px solid #e5e7eb !important;
    padding: 14px 52px 14px 14px !important;
    font-size: 14px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    outline: none !important;
}

div[data-testid="stChatInput"] button {
    position: absolute !important;
    right: 18px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #6b7280 !important;
}

div[data-testid="stChatInput"] button:hover {
    color: #111827 !important;
}

[data-theme="dark"] div[data-testid="stChatInput"] textarea {
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
    border: 1px solid #374151 !important;
}

[data-theme="dark"] div[data-testid="stChatInput"] button {
    color: #9ca3af !important;
}

[data-theme="dark"] div[data-testid="stChatInput"] button:hover {
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================================
# CONFIGURAÇÕES (DIALOG)
# ============================================================================

@st.dialog("⚙️ Configurações")
def config_dialog():

    st.session_state.tema = st.selectbox(
        "Tema",
        ["Claro", "Escuro"],
        index=0 if st.session_state.tema == "Claro" else 1
    )

    st.markdown("---")

    if st.button("Salvar", use_container_width=True):
        st.success("Configurações salvas!")
        st.rerun()


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
    st.metric("Execuções", stats.get("total_function_calls", 0))
    st.metric("Mensagens", stats.get("total_messages", 0))
    st.metric("Logs", stats.get("total_logs", 0))
    st.metric("Erros", stats.get("errors", 0))

    st.divider()

    if st.button("Configurações", use_container_width=True):
        config_dialog()


# ============================================================================
# LAYOUT
# ============================================================================

tab_chat, tab_logs, tab_charts, tab_docs = st.tabs(
    ["💬 Chat", "📋 Logs", "📈 Charts", "📖 Docs"]
)


with tab_chat:

    col_chat, col_debug = st.columns([3, 1])


    # ============================================================================
    # CHAT
    # ============================================================================

    with col_chat:

        chat_container = st.container(height=500)

    # ----------------------------
    # INPUT
    # ----------------------------
    if prompt := st.chat_input("Digite sua mensagem..."):

        # Log da mensagem do usuário
        logger.log_message("user", prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        intent = identificar_intencao(prompt)
        layout = identificar_layout(prompt)

        # Executar ação e medir tempo
        with st.spinner("Pensando..."):
            start = time.time()
            try:
                resposta = executar_acao(intent)
                error = None
            except Exception as e:
                resposta = f"❌ Erro: {e}"
                error = str(e)
            exec_time = (time.time() - start) * 1000

        # Registrar execução no logger e nas métricas
        try:
            logger.log_function_call(
                function_name="executar_acao",
                params={"intent": intent},
                result=resposta,
                error=error,
                execution_time_ms=exec_time
            )
        except Exception:
            pass

        try:
            st.session_state.metrics.track_execution(
                function_name="executar_acao",
                params={"intent": intent},
                result=resposta,
                execution_time_ms=exec_time,
                error=error
            )
        except Exception:
            pass

        # Armazenar métrica para exibição simples
        st.session_state.execution_metrics.append({
            "input": prompt,
            "exec_time": exec_time,
            "timestamp": datetime.now().isoformat()
        })

        # Log da resposta do assistant
        logger.log_message("assistant", str(resposta))

        st.session_state.messages.append({
            "role": "assistant",
            "layout": layout,
            "content": resposta
        })

    # ----------------------------
    # RENDER CHAT
    # ----------------------------
    with chat_container:

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):

                if msg["role"] == "user":
                    st.markdown(msg["content"])
                else:
                    renderizar_resposta(
                        msg["layout"],
                        msg["content"]
                    )


with tab_logs:

    st.markdown("### Logs")

    logs = logger.get_all_logs()

    if logs:
        df = pd.DataFrame(logs)
        df = df.astype(str)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum log ainda")


with tab_charts:

    st.markdown("### Performance")

    func_logs = logger.get_function_logs()

    if func_logs:

        times = [l.get("execution_time_ms", 0) for l in func_logs]

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=times, mode="lines+markers"))

        st.plotly_chart(fig, use_container_width=True)

    else:
        # Fallback para métricas coletadas em session_state
        hist = getattr(st.session_state.metrics, "execution_history", [])
        if hist:
            times = [e.get("execution_time_ms", 0) for e in hist]
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=times, mode="lines+markers"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados")


with tab_docs:

    st.markdown("### 📖 Documentação")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        **Objetivo**

        Este chat integra:
        - Comunicação com banco (gel)
        - Function calling
        - Logging estruturado
        - Observabilidade mínima
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        **Fluxo**

        1. Usuário envia mensagem  
        2. Identifica intenção  
        3. Executa ação via `executar_acao`  
        4. Registra logs e métricas  
        5. Retorna resposta  
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        **Funções principais**

        - `executar_acao(intent)` — lógica de controle e DB
        - `logger` — registros de mensagens e funções
        - `ExecutionMetrics` — histórico de execuções
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="text-align:center;color:#999;">
    Chat (DB) • Métricas incorporadas
    </div>
    """, unsafe_allow_html=True)