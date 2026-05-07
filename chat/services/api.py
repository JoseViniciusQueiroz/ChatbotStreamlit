import requests

API_URL = "http://app:8000"

def listar_empregados():
    response = requests.get(
        f"{API_URL}/Empregados"
    )
    if response.status_code != 200:
        return "Erro ao consultar empregados."
    dados = response.json()
    return dados


def listar_gerentes():
    response = requests.get(
        f"{API_URL}/Gerentes"
    )
    if response.status_code != 200:
        return "Erro ao consultar gerentes."
    dados = response.json()
    return dados


def listar_areas():
    response = requests.get(
        f"{API_URL}/Area"
    )
    if response.status_code != 200:
        return "Erro ao consultar áreas."
    dados = response.json()
    return dados
