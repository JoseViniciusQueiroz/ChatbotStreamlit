from services.api import (
    listar_empregados,
    listar_gerentes,
    listar_areas
)


INTENTS = {

    "LISTAR_EMPREGADOS": {
        "palavras": [
            "empregado",
            "empregados",
            "funcionario",
            "funcionários"
        ],
        "funcao": listar_empregados
    },

    "LISTAR_GERENTES": {

        "palavras": [
            "gerente",
            "gerentes",           
        ],
        "funcao": listar_gerentes
    },

    "LISTAR_AREAS": {
        "palavras":[
            "área",
            "area",
            "areas"
        ],
        "funcao": listar_areas

    }
}