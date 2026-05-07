# 🚀 Quick Start Guide

Comece a usar o **AI Agent com Function Calling** em 5 minutos!

## 📦 Pré-requisitos

- Python 3.11+
- pip ou conda

## ⚡ Instalação Rápida

### 1. Instalar Dependências

```bash
cd chat2
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run main.py
```

A aplicação abrirá em: **http://localhost:8501**

## 🎮 Primeiros Passos

### Você está agora na interface Streamlit!

#### Aba "💬 Chat"
Digite exemplos como:
- `"Quanto é 5 vezes 3?"`
- `"Arredondar 3.14159"`
- `"Olá João"`

#### Aba "📋 Logs"
- Veja todos os logs de execução
- Exporte em JSON
- Acompanhe métricas em tempo real

#### Aba "📖 Documentação"
- Aprenda sobre o sistema
- Veja arquitetura
- Explore extensões futuras

## 🧪 Executar Testes

```bash
# Testes unitários
python -m pytest test_module.py -v

# Ou com unittest
python -m unittest test_module.py
```

## 📝 Executar Exemplos

```bash
python examples.py
```

Isso rodará 8 exemplos diferentes mostrando:
- Multiplicação
- Arredondamento
- Saudação
- Tratamento de erros
- Logging completo
- E mais!

## 🐳 Com Docker

```bash
# Build
docker build -t chat2:latest .

# Run
docker run -p 8502:8502 chat2:latest
```

## 📊 Estrutura de Arquivos

```
chat2/
├── main.py          ← Aplicação Streamlit (START HERE!)
├── agent.py         ← Lógica de IA
├── functions.py     ← Funções registradas
├── logger.py        ← Sistema de logs
├── examples.py      ← Exemplos de uso
├── test_module.py   ← Testes unitários
├── requirements.txt ← Dependências
├── dockerfile       ← Para containerização
└── README.md        ← Documentação completa
```

## 🎯 Exemplo Rápido em Python

```python
from agent import AIAgent
from logger import logger

# Criar agent
agent = AIAgent()

# Processar mensagem
response, metadata = agent.process_message("Quanto é 10 vezes 20?")

# Usar resultado
print(response)
print(f"Resultado: {metadata['result']}")
print(f"Tempo: {metadata['execution_time_ms']}ms")

# Ver logs
stats = logger.get_stats()
print(stats)
```

## 💡 Próximos Passos

1. ✅ Explore a interface Streamlit
2. ✅ Rode os exemplos em `examples.py`
3. ✅ Estude os testes em `test_module.py`
4. ✅ Customize as funções em `functions.py`
5. ✅ Expanda a detecção de intenção em `agent.py`
6. ✅ Integre com OpenAI/Claude

## 🔧 Adicionar Nova Função

**1. Em `functions.py`:**

```python
def minha_funcao(parametro: str) -> str:
    """Minha função personalizada"""
    return f"Resultado: {parametro}"

# Registrar
registry.register("minha_funcao", minha_funcao)
```

**2. Em `agent.py`:**

```python
"minha_intencao": {
    "keywords": ["palavra-chave"],
    "function": "minha_funcao",
    "params_pattern": r'(\w+)',
    "param_names": ["parametro"]
}
```

## 🚨 Troubleshooting

### Erro: "streamlit: comando não encontrado"
```bash
# Instale corretamente
pip install streamlit pandas
```

### Erro: "No module named 'agent'"
```bash
# Certifique-se de estar na pasta chat2
cd chat2
```

### Porta 8501 já em uso?
```bash
streamlit run main.py --server.port 8503
```

## 📚 Recursos Adicionais

- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Nosso README](README.md)

## 🎉 Parabéns!

Você já tem um AI Agent funcional! Agora é hora de explorar, customizar e expandir! 🚀

---

**Tem dúvidas? Veja o README.md para documentação completa.**
