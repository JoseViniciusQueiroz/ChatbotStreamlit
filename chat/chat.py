import streamlit as st

from intents.parser import (
    identificar_intencao,
    identificar_layout
)

from core.executer import (
    executar_acao,
    renderizar_resposta
)

st.set_page_config(page_title="Chat", layout="wide")

st.title("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tema" not in st.session_state:
    st.session_state.tema = "Claro"

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
    if st.button("Configurações", use_container_width=True):
        config_dialog()


# ============================================================================
# LAYOUT
# ============================================================================

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

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        intent = identificar_intencao(prompt)
        layout = identificar_layout(prompt)

        with st.spinner("Pensando..."):
            resposta = executar_acao(intent)

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