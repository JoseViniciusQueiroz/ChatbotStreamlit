
import streamlit as st

from intents.intents import INTENTS
from renders.registry import RENDERERS


def renderizar_resposta(layout, dados):
    render_func = RENDERERS.get(layout)
    if not render_func:
        st.error(
            f"Layout '{layout}' não suportado."
        )
        return
    render_func(dados)


def executar_acao(intent):
    if not intent:
        return "Não entendi."
    funcao = INTENTS[intent]["funcao"]
    return funcao()
