# 🤖 AI Agent com Function Calling - MVP

Uma aplicação de teste construída com **Streamlit** focado em simulação de IA, **function calling** e **observabilidade via logs**.

## 📋 O que é este projeto?

Este é um MVP (Minimum Viable Product) que demonstra:

- ✅ **Chat com IA**: Interface de conversação com interpretação de intenção
- ✅ **Function Calling**: Execução dinâmica de funções baseada em intenção do usuário
- ✅ **Logging Avançado**: Registro detalhado de todas as interações com timestamps e métricas
- ✅ **Observabilidade**: Dashboard com estatísticas e histórico de execução

## 🎯 Objetivo

Servir como base sólida para:
- Testes de integração com APIs de IA (OpenAI, Claude, etc.)
- Desenvolvimento de agents mais sofisticados
- Prototipagem rápida de chatbots
- Aprendizado de padrões de function calling

## 📂 Estrutura do Projeto

```
chat2/
├── main.py              # Aplicação principal (Streamlit)
├── agent.py             # Lógica de IA e decisão de funções
├── functions.py         # Registro e execução de funções
├── logger.py            # Sistema de logging e observabilidade
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 🚀 Como Executar

### 1. Instalação

```bash
# Navegar para a pasta
cd chat2

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
streamlit run main.py
```

A aplicação abrirá em `http://localhost:8501`

### 3. Usar o Docker (Opcional)

Você pode adicionar um novo serviço ao seu `docker-compose.yml`:

```yaml
app_chat2:
  build:
    context: ./chat2
  command: streamlit run main.py --server.port 8503 --server.address 0.0.0.0
  ports:
    - "8503:8503"
  volumes:
    - ./chat2:/app
```

Depois execute:
```bash
docker-compose up app_chat2
```

## 🎮 Como Usar

### Chat
1. Abra a aba **💬 Chat**
2. Digite sua mensagem (exemplos: "quanto é 5 vezes 3?", "olá João", "arredondar 3.14159")
3. Clique em **📤 Enviar**
4. Veja a resposta do agent e o tempo de execução

### Logs
1. Abra a aba **📋 Logs**
2. Filtre por tipo: Todos, Funções ou Mensagens
3. Veja detalhes de cada execução
4. Exporte os logs em JSON para análise

### Documentação
1. Abra a aba **📖 Documentação**
2. Leia sobre a arquitetura e funções disponíveis

## 🔧 Funções Disponíveis

### 1. **Multiplicar**
Multiplica dois números.

**Como usar:**
```
"Quanto é 5 vezes 3?"
"Multiplicar 10 por 7"
"2 × 8"
```

**Exemplo de resposta:**
```
✅ Resultado: 5 × 3 = 15
⏱️ Tempo: 0.12ms
```

### 2. **Calcular Decimal**
Arredonda um número para 10 casas decimais.

**Como usar:**
```
"Arredondar 3.14159"
"Decimal de 2.71828"
```

**Exemplo de resposta:**
```
✅ Resultado: 3.14159 arredondado para 10 casas = 3.1415900000
⏱️ Tempo: 0.08ms
```

### 3. **Saudação**
Retorna uma saudação personalizada.

**Como usar:**
```
"Olá João"
"Oi Maria"
```

**Exemplo de resposta:**
```
✅ Olá João! 👋 Seja bem-vindo ao nosso assistente!
⏱️ Tempo: 0.05ms
```

## 📊 Sistema de Logging

### Estrutura de um Log

#### Log de Função:
```json
{
  "timestamp": "2026-01-01 10:00:00",
  "function": "multiplicar",
  "params": {"a": 5, "b": 3},
  "result": 15,
  "error": null,
  "execution_time_ms": 0.12
}
```

#### Log de Mensagem:
```json
{
  "timestamp": "2026-01-01 10:00:00",
  "type": "user",
  "content": "Quanto é 5 vezes 3?",
  "user_id": null
}
```

### Recursos de Logging

- 📝 Registro automático de todas as interações
- ⏱️ Medição de tempo de execução
- 📊 Estatísticas em tempo real
- 📥 Exportação em JSON
- 🔍 Filtros e buscas

## 🧠 Como Funciona a Detecção de Intenção

O sistema usa um padrão simples mas eficaz:

```
1. Receber entrada do usuário
   ↓
2. Buscar palavras-chave na entrada
   ↓
3. Mapear palavra-chave para intenção
   ↓
4. Extrair parâmetros usando regex
   ↓
5. Validar parâmetros
   ↓
6. Executar função correspondente
   ↓
7. Registrar em logs
   ↓
8. Retornar resultado
```

## 🛠️ Extensão do Projeto

### Adicionar Nova Função

**1. Criar a função em `functions.py`:**
```python
def nova_funcao(parametro: str) -> str:
    """Descrição da função"""
    return f"Resultado: {parametro}"
```

**2. Registrar no `FunctionRegistry`:**
```python
def _register_default_functions(self):
    self.register("nova_funcao", nova_funcao)
    # ...
```

**3. Adicionar intent em `agent.py`:**
```python
self.intent_keywords = {
    # ...
    "nova_intencao": {
        "keywords": ["palavra-chave1", "palavra-chave2"],
        "function": "nova_funcao",
        "params_pattern": r'(\w+)',
        "param_names": ["parametro"]
    }
}
```

### Integrar com API de IA Real (OpenAI)

```python
import openai

def process_message_with_gpt(self, user_input: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente útil"},
            {"role": "user", "content": user_input}
        ],
        functions=self.get_function_definitions()
    )
    # ... processar resposta
```

## 📈 Estatísticas

A aplicação fornece estatísticas em tempo real:

- 📝 Total de logs registrados
- 🔧 Número de funções executadas
- 💬 Total de mensagens
- ❌ Número de erros
- 📊 Funções mais chamadas
- ⏱️ Tempo médio de execução

## 🔐 Segurança

- ✅ Validação de entrada com regex
- ✅ Prevenção de injeção com parâmetros tipados
- ✅ Tratamento de exceções
- ✅ Logging de erros

## 🎨 Interface

A aplicação possui:

- 🎯 Design limpo e intuitivo
- 🌈 Gradientes e cores harmoniosas
- 📱 Layout responsivo
- 🔄 Atualização em tempo real
- 🎭 Temas customizáveis

## 💾 Persistência

Atualmente, os logs são mantidos em memória durante a sessão.

**Para persistir em banco de dados:**

```python
# Em logger.py
import sqlite3

def save_to_db(self, db_path="logs.db"):
    conn = sqlite3.connect(db_path)
    for log in self.logs:
        # Salvar log no banco
    conn.commit()
    conn.close()
```

## 🐛 Debugging

### Ativar modo verbose:
```python
# Em agent.py
DEBUG = True

if DEBUG:
    print(f"Intent detectada: {intent}")
    print(f"Parâmetros extraídos: {params}")
```

## 📚 Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Python Regex](https://docs.python.org/3/library/re.html)

## 🤝 Contribuições

Este é um projeto de aprendizado. Sinta-se livre para:

- Adicionar novas funções
- Melhorar detecção de intenção
- Implementar persistência
- Expandir para IA real
- Otimizar performance

## 📜 Licença

MIT License - Use livremente!

## ✨ Features Planejadas

- [ ] Integração com OpenAI/Claude
- [ ] Persistência em banco de dados
- [ ] Análise de sentimento
- [ ] Histórico por usuário
- [ ] Dashboard de analytics
- [ ] Webhooks
- [ ] Rate limiting
- [ ] Multi-idioma

## 🎉 Conclusão

Este MVP fornece uma base sólida para explorar function calling, logging avançado e desenvolvimento de agents. Sinta-se livre para modificar, estender e integrar com sistemas mais complexos!

---

**Desenvolvido com ❤️ usando Python e Streamlit**
