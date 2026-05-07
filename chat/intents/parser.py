from intents.intents import INTENTS
from intents.layouts import LAYOUTS


def identificar_intencao(prompt):
    prompt = prompt.lower()
    for intent, dados in INTENTS.items():
        for palavra in dados["palavras"]:
            if palavra in prompt:
                return intent
    return None

def identificar_layout(prompt):
    prompt = prompt.lower()
    for layout, palavras in LAYOUTS.items():
        for palavra in palavras:
            if palavra in prompt:
                return layout
    return "text"