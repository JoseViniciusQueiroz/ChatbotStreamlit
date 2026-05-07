import streamlit as st

CAMPOS_OCULTOS = [
    "id"
]

def formatar_chave(chave):
    nomes = {
        "cpfPessoa": "CPF",
        "nomePessoa": "Nome"
    }
    return nomes.get(chave, chave)
def render_text(dados):
    if not isinstance(dados, list):

        st.write(dados)

        return

    for item in dados:

        linhas = []

        for chave, valor in item.items():

            if chave in CAMPOS_OCULTOS:
                continue

            chave_formatada = formatar_chave(chave)

            linhas.append(
                f"**{chave_formatada}:** {valor}"
            )

        st.markdown(
            "  \n".join(linhas)
        )

        st.divider()