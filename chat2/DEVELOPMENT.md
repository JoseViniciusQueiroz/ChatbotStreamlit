# 🛠️ Guia de Desenvolvimento

Instruções para contribuir e expandir o projeto.

## 🎯 Antes de Começar

1. Leia o [README.md](README.md)
2. Explore [QUICKSTART.md](QUICKSTART.md)
3. Estude [ANALYSIS.md](ANALYSIS.md)
4. Rode os [examples.py](examples.py)
5. Rode os testes: `python test_module.py`

## 🏗️ Arquitetura Modular

```
┌─────────────────────────────────────┐
│         main.py (Streamlit UI)       │
├─────────────────────────────────────┤
│      agent.py (Decision Logic)       │
│  (Detect Intent → Extract Params)    │
├─────────────────────────────────┬────┤
│   functions.py (Function Exec)   │    │
│   (Registry + Mock Functions)    │    │
├─────────────────────────────────┤    │
│    logger.py (Observability)     │    │
│  (Logs + Metrics + Export)       │    │
└─────────────────────────────────┴────┘
```

## 📝 Adicionar Nova Função

### Exemplo: Função "Dividir"

**1. Implementar em `functions.py`:**

```python
def dividir(a: float, b: float) -> float:
    """
    Divide dois números
    
    Args:
        a: Dividendo
        b: Divisor
    
    Returns:
        Resultado da divisão
    
    Raises:
        ValueError: Se b for zero
    """
    if b == 0:
        raise ValueError("Divisor não pode ser zero")
    return float(a / b)
```

**2. Registrar em `FunctionRegistry._register_default_functions()`:**

```python
def _register_default_functions(self):
    self.register("multiplicar", multiplicar)
    self.register("calcular_decimal", calcular_decimal)
    self.register("saudacao", saudacao)
    self.register("dividir", dividir)  # ← NOVA
```

**3. Adicionar à lista de descrições:**

```python
def list_functions(self) -> Dict[str, str]:
    return {
        "multiplicar": "Multiplica dois números: multiplicar(a, b)",
        "calcular_decimal": "Arredonda um número para 10 casas decimais: calcular_decimal(valor)",
        "saudacao": "Retorna uma saudação personalizada: saudacao(nome)",
        "dividir": "Divide dois números: dividir(a, b)"  # ← NOVA
    }
```

**4. Adicionar teste em `test_module.py`:**

```python
def test_dividir(self):
    """Testa divisão"""
    self.assertEqual(dividir(10, 2), 5)
    self.assertEqual(dividir(15, 3), 5)
    
    with self.assertRaises(ValueError):
        dividir(10, 0)
```

---

## 🧠 Adicionar Nova Intenção

### Exemplo: Intenção "Dividir"

**1. Em `agent.py`, adicionar ao dicionário `self.intent_keywords`:**

```python
self.intent_keywords = {
    # ... existentes ...
    "dividir": {
        "keywords": ["dividir", "divisão", "/", "por"],
        "function": "dividir",
        "params_pattern": r'(\d+\.?\d*)\s*(?:dividir|\/)\s*(\d+\.?\d*)',
        "param_names": ["a", "b"]
    }
}
```

**2. Adicionar testes:**

```python
def test_intent_detection_dividir(self):
    """Testa detecção de divisão"""
    intent = self.agent.detect_intent("quanto é 10 dividido por 2")
    self.assertEqual(intent, "dividir")

def test_parameter_extraction_dividir(self):
    """Testa extração de parâmetros"""
    params = self.agent.extract_parameters("10 dividir 2", "dividir")
    self.assertEqual(params["a"], 10.0)
    self.assertEqual(params["b"], 2.0)
```

---

## 🧪 Testes

### Executar Todos os Testes

```bash
# Com unittest
python -m unittest test_module.py -v

# Com pytest (se instalado)
pytest test_module.py -v

# Com coverage
coverage run -m unittest test_module.py
coverage report
```

### Estrutura de um Teste

```python
class TestMinhaFuncionalidade(unittest.TestCase):
    """Descrição da funcionalidade testada"""
    
    def setUp(self):
        """Configuração antes de cada teste"""
        self.agent = AIAgent()
    
    def test_caso_sucesso(self):
        """Testa caso de sucesso"""
        result = self.agent.detect_intent("input")
        self.assertEqual(result, "expected")
    
    def test_caso_falha(self):
        """Testa caso de falha"""
        result = self.agent.detect_intent("invalid")
        self.assertIsNone(result)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        pass
```

---

## 📊 Melhorar Detecção de Intenção

### Atual (Regex Simples)
```python
params_pattern = r'(\d+\.?\d*)\s*(?:dividir|\/)\s*(\d+\.?\d*)'
```

### Alternativa 1: NLP com NLTK
```python
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_numbers(text):
    """Extrai números do texto"""
    import re
    return re.findall(r'\d+\.?\d*', text)
```

### Alternativa 2: LLM Integration
```python
import openai

def detect_intent_with_gpt(user_input: str) -> str:
    """Detecta intenção usando GPT"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Detect the user's intent..."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content
```

---

## 💾 Persistência de Logs

### SQLite
```python
# Em logger.py
import sqlite3
from datetime import datetime

def save_to_sqlite(self, db_path="logs.db"):
    """Salva logs em SQLite"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            function TEXT,
            params TEXT,
            result TEXT,
            error TEXT,
            execution_time_ms REAL
        )
    ''')
    
    # Inserir logs
    for log in self.get_function_logs():
        cursor.execute('''
            INSERT INTO logs 
            (timestamp, function, params, result, error, execution_time_ms)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            log.get('timestamp'),
            log.get('function'),
            str(log.get('params')),
            str(log.get('result')),
            log.get('error'),
            log.get('execution_time_ms')
        ))
    
    conn.commit()
    conn.close()
```

### MongoDB
```python
from pymongo import MongoClient

def save_to_mongodb(self, connection_string="mongodb://localhost:27017/"):
    """Salva logs em MongoDB"""
    client = MongoClient(connection_string)
    db = client['chat_ai']
    collection = db['logs']
    
    collection.insert_many(self.get_all_logs())
    client.close()
```

---

## 🔌 Integração com OpenAI

### Setup

```bash
pip install openai
export OPENAI_API_KEY="sua-chave-aqui"
```

### Implementação

```python
# Em agent.py (adicionar)
import openai

class AIAgentGPT(AIAgent):
    """Agent usando GPT para detecção e extração"""
    
    def detect_intent_gpt(self, user_input: str) -> Optional[str]:
        """Detecta intenção usando GPT"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an intent classifier. Available intents: multiplicar, calcular_decimal, saudacao. Respond with just the intent name or None."
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    
    def extract_parameters_gpt(self, user_input: str, intent: str) -> Dict[str, Any]:
        """Extrai parâmetros usando GPT"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Extract parameters for intent: {intent}. Return JSON format."
                },
                {"role": "user", "content": user_input}
            ]
        )
        # Parse JSON response
        import json
        return json.loads(response.choices[0].message.content)
```

---

## 🚀 Deploy

### Heroku

```bash
# 1. Criar Procfile
echo "web: streamlit run main.py --server.port=\$PORT --server.address 0.0.0.0" > Procfile

# 2. Deploy
heroku create seu-app-name
git push heroku main
```

### Docker Compose

```yaml
# Adicionar ao docker-compose.yml
app_chat2:
  build:
    context: ./chat2
  command: streamlit run main.py --server.port 8503 --server.address 0.0.0.0
  ports:
    - "8503:8503"
  volumes:
    - ./chat2:/app
  environment:
    - PYTHONUNBUFFERED=1
```

---

## 📈 Performance

### Otimizações

```python
# 1. Cache de intent detection
from functools import lru_cache

@lru_cache(maxsize=128)
def detect_intent(self, user_input: str) -> Optional[str]:
    # ... implementação
    pass

# 2. Async operations
import asyncio

async def process_message_async(self, user_input: str):
    """Versão async para melhor performance"""
    intent = await asyncio.to_thread(self.detect_intent, user_input)
    params = await asyncio.to_thread(self.extract_parameters, user_input, intent)
    result = await asyncio.to_thread(registry.execute, ...)
    return result

# 3. Profiling
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... código a otimizar ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

---

## 🐛 Debugging

### Modo Verbose

```python
# Em agent.py
DEBUG = True

if DEBUG:
    print(f"[DEBUG] Input: {user_input}")
    print(f"[DEBUG] Intent: {intent}")
    print(f"[DEBUG] Params: {params}")
    print(f"[DEBUG] Result: {result}")
```

### Logging com Python Logger

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Processing: {user_input}")
logger.info(f"Intent detected: {intent}")
logger.error(f"Error: {error}")
```

---

## 📚 Documentação

### Docstrings (Google Style)

```python
def minha_funcao(parametro: str) -> str:
    """
    Descrição breve em uma linha.
    
    Descrição longa se necessário. Pode ser múltiplas linhas.
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando algo dá errado
    
    Example:
        >>> minha_funcao("teste")
        "resultado"
    """
    pass
```

---

## ✅ Checklist para Novo Feature

- [ ] Implementar a função
- [ ] Adicionar ao registry
- [ ] Implementar intent detection
- [ ] Implementar parameter extraction
- [ ] Escrever testes unitários
- [ ] Testar manualmente na UI
- [ ] Documentar em README.md
- [ ] Adicionar exemplo em examples.py
- [ ] Commit e push

---

## 🤝 Code Style

```python
# Usar type hints
def process_message(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
    pass

# Usar f-strings
message = f"Resultado: {result}"

# Comentários explicativos
# Bom:
# Incrementar o contador de tentativas
attempts += 1

# Ruim:
attempts += 1  # <- não explica o porquê

# Linha máxima: 100 caracteres
# Quebrar linhas longas de forma legível

# Usar type hints em tudo
from typing import Dict, List, Optional
```

---

## 🎓 Recursos de Aprendizado

- [Real Python - Function Calling](https://realpython.com/)
- [OpenAI Docs](https://platform.openai.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Clean Code (Robert Martin)](https://en.wikipedia.org/wiki/Robert_C._Martin)
- [Design Patterns (Gang of Four)](https://en.wikipedia.org/wiki/Design_Patterns)

---

## 📞 Suporte

Dúvidas? Consulte:
1. [README.md](README.md) - Documentação geral
2. [QUICKSTART.md](QUICKSTART.md) - Começar rápido
3. [ANALYSIS.md](ANALYSIS.md) - Comparação com chat/
4. [examples.py](examples.py) - Exemplos práticos
5. Código documentado com docstrings

---

**Happy Coding! 🚀**
