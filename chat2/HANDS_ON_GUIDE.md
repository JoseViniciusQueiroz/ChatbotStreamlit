# 🎬 Guia Prático - Teste as Métricas em 5 Minutos

## 📦 Setup Inicial

```bash
cd chat2

# 1. Instalar dependências (inclui Plotly para gráficos)
pip install -r requirements.txt

# 2. Rodar a aplicação
streamlit run main.py
```

Browser abrirá em: **http://localhost:8501**

## 🎯 O Que Você Verá

### 1️⃣ Na Primeira Abertura
```
SIDEBAR (Esquerda):
├─ ⚙️ Controles: Limpar | Logs
├─ 📊 Métricas em Tempo Real
│   ├─ Execuções: 0
│   ├─ Mensagens: 0
│   ├─ Logs Total: 0
│   ├─ Erros: 0
│   └─ ⏱️ Latência: (vazio - sem dados)
├─ 📈 Performance (gráfico vazio)
├─ 🔧 Ferramentas (gráfico vazio)
└─ 💡 Dicas

MAIN (Centro):
└─ 4 ABAS: 💬 Chat | 📋 Logs | 📈 Charts | 📖 Docs
```

### 2️⃣ Digite na Aba "Chat"

**EXEMPLOS:**

```
"5 vezes 3"
↓
🤖 Agent:
✅ Resultado: 5 × 3 = 15
⏱️ Tempo: 0.95ms

════════════════════════════════

"Arredondar 3.14159"
↓
🤖 Agent:
✅ Resultado: arredondado para 10 casas = 3.1415900000
⏱️ Tempo: 1.23ms

════════════════════════════════

"Olá João"
↓
🤖 Agent:
✅ Olá João! 👋 Seja bem-vindo!
⏱️ Tempo: 0.88ms
```

### 3️⃣ Veja as Métricas Atualizarem

Após cada execução no chat, você verá:

**SIDEBAR (Atualizado em tempo real):**
```
📊 Métricas em Tempo Real
├─ Execuções: 3 ⬆️
├─ Mensagens: 3 ⬆️
├─ Logs Total: 9 ⬆️
├─ Erros: 0
└─ ⏱️ Latência Média: 1.02ms ⬆️
```

**GRÁFICOS NA SIDEBAR (Aparecem)**
```
📈 Performance
├─ Gráfico de linha com 3 pontos
│  (0.95ms → 1.23ms → 0.88ms)
└─ Mostra tendência

🔧 Ferramentas
├─ Gráfico de barras
├─ multiplicar: 1
├─ saudacao: 1
└─ calcular_decimal: 1
```

### 4️⃣ Clique na Aba "Logs"

Verá uma tabela com TODOS os eventos:

```
┌────────────┬────┬──────────┬────────────┬──────────┬────────────┐
│ Hora       │ ID │ Função   │ Parâmetros │ Resultado│ Tempo      │
├────────────┼────┼──────────┼────────────┼──────────┼────────────┤
│ 10:30:45   │ 🔧 │multipli. │ a=5, b=3   │ 15       │ 0.95ms     │
│ 10:30:44   │ 💬 │USER      │ -          │ 5 vezes 3│ -          │
│ 10:30:44   │ 🤖 │ASSISTANT │ -          │ Resultado│ -          │
│ 10:30:40   │ 🔧 │arredon.  │ valor=3.14 │ 3.14159  │ 1.23ms     │
│ ... (mais) │    │          │            │          │            │
└────────────┴────┴──────────┴────────────┴──────────┴────────────┘

Filtros: [Todos ▼]  📥 Exportar  🔄 Atualizar

Estatísticas
Total | Funções | Mensagens | Erros
  9   |    3    |     6     |   0
```

### 5️⃣ Clique na Aba "Charts" ⭐

Dashboard profissional com:

```
KPIs:
┌──────────────┬──────────┬──────────┬────────────┐
│ Total Exec.  │ Lat Avg  │ Lat Max  │ Taxa Erro  │
│ 3            │ 1.02ms   │ 1.23ms   │ 0.0%       │
└──────────────┴──────────┴──────────┴────────────┘

Performance ao Longo do Tempo | Distribuição de Uso
┌─────────────────────────────┬─────────────────────┐
│         (Gráfico 1)         │   (Gráfico 2)       │
│  Linha com 3 pontos:        │  Pizza de 3 fatias: │
│  0.95 → 1.23 → 0.88         │  multiplicar: 33%   │
│                             │  saudacao: 33%      │
│                             │  calcular_: 33%     │
└─────────────────────────────┴─────────────────────┘

Histórico Detalhado de Execuções:
# │ Função   │ Tempo(ms) │ Parâmetros  │ Status │ Hora
─────────────────────────────────────────────────────
1 │ multipli.│ 0.95      │ a=5, b=3    │ ✓      │ 10:30:45
2 │ arredon. │ 1.23      │ valor=3.14  │ ✓      │ 10:30:40
3 │ saudacao │ 0.88      │ nome=João   │ ✓      │ 10:30:35

Tempo Médio por Ferramenta:
Ferramenta      │ Avg (ms) │ Min (ms) │ Max (ms)
─────────────────────────────────────────────
multiplicar     │ 0.95     │ 0.95     │ 0.95
calcular_decimal│ 1.23     │ 1.23     │ 1.23
saudacao        │ 0.88     │ 0.88     │ 0.88

Taxa de Sucesso por Ferramenta:
Ferramenta      │ Sucesso │ Total │ Taxa (%)
─────────────────────────────────────────
multiplicar     │ 1       │ 1     │ 100.0%
calcular_decimal│ 1       │ 1     │ 100.0%
saudacao        │ 1       │ 1     │ 100.0%
```

### 6️⃣ Clique em "Exportar" (Aba Logs)

Download de `logs.json`:

```json
[
  {
    "timestamp": "2024-05-07 10:30:45",
    "type": "user",
    "content": "5 vezes 3"
  },
  {
    "timestamp": "2024-05-07 10:30:45",
    "function": "multiplicar",
    "params": {"a": 5.0, "b": 3.0},
    "result": 15.0,
    "error": null,
    "execution_time_ms": 0.95
  },
  ...
]
```

## 🎮 Interatividade

### Gráficos Plotly (Interativos)

Ao passar mouse sobre qualquer gráfico:
- ✅ Hover tooltip com valores
- ✅ Zoom (arrastar para ampliar)
- ✅ Pan (shift + arrastar)
- ✅ Reset (duplo clique)
- ✅ Download como PNG

### Tabelas

- ✅ Scroll horizontal/vertical
- ✅ Sortable (clique no header)
- ✅ Altura customizável
- ✅ Expandir em tela cheia

## 🔄 Fluxo Completo: Passo a Passo

```
1. Abre aplicação
   ↓ Sidebar vazio
   ↓ MAIN mostra Chat

2. Digita no input: "5 vezes 3"
   ↓ Clica "↩️ Enviar"
   ↓ Processamento:
     - Detecta intent: "multiplicar"
     - Extrai params: a=5, b=3
     - Executa função
     - Calcula tempo: 0.95ms
     - Log registrado

3. Resposta aparece:
   ✅ Resultado: 5 × 3 = 15
   ⏱️ Tempo: 0.95ms

4. Sidebar atualiza:
   - Execuções: 1
   - Gráficos aparecem com 1 ponto

5. Aba "Logs":
   - Mostra 3 logs (user, assistant, function)

6. Aba "Charts":
   - KPI com 1 execução
   - Gráficos com 1 ponto

7. Repete passos 2-6 mais vezes
   - Gráficos ficar mais interessantes
   - Médias começam a aparecer
   - Distribuição fica visível
```

## 🎯 Teste Prático (Sugerido)

**Execute estas operações na ordem:**

```
1º: "2 vezes 10"      → Multiplicação
2º: "Olá Maria"       → Saudação
3º: "3 vezes 7"       → Multiplicação
4º: "Arredondar 2.71" → Decimal
5º: "Oi Roberto"      → Saudação
6º: "4 × 5"           → Multiplicação
```

**Resultado esperado:**
- 6 execuções totais
- 3 multiplicações (50%)
- 2 saudações (33%)
- 1 decimal (17%)
- 100% de sucesso
- Latência média ~1ms

**No Dashboard:**
```
Total Exec: 6
Lat Avg: 1.00ms
Taxa Erro: 0.0%

Pizza 3D: multiplicar 50%, saudacao 33%, calcular 17%
Timeline: 6 pontos ascendentes
Tabela: 6 linhas com tempos
```

## 💾 Botões Importantes

| Botão | Encontrado | Função |
|-------|-----------|--------|
| 🔄 Limpar | Sidebar | Apaga chat + métricas |
| 🗑️ Logs | Sidebar | Limpa todos os logs |
| 📥 Exportar | Aba Logs | Download JSON dos logs |
| 🔄 Atualizar | Aba Logs | Recarrega dados |
| ↩️ Enviar | Aba Chat | Envia mensagem |

## 📊 Dados Que Aparecem

### Real-time (Atualizam instantaneamente)
- ✅ Sidebar metrics
- ✅ Chat messages
- ✅ Sidebar charts

### On-demand (Carregam ao clicar)
- ✅ Aba Logs (tabela)
- ✅ Aba Charts (dashboard)

## 🎓 O Que Aprender

Observando a aplicação:

1. **Performance Monitoring**: Como track latência
2. **Metrics Visualization**: Gráficos + tabelas
3. **Dashboard Design**: KPIs + trends + details
4. **Real-time Updates**: Sidebar atualiza sem reload
5. **Data Export**: JSON para análise externa
6. **User Experience**: Feedback visual de execução

## 🚀 Próximas Etapas

Depois de testar:

1. **Adicionar mais funções** (em `functions.py`)
2. **Integrar OTEL** (descomente em `observability.py`)
3. **Configurar Jaeger** (docker run ...)
4. **Adicionar persistência** (PostgreSQL)
5. **Buildar dashboard Grafana** (Prometheus)

---

**Aproveita! A interface é profissional, responsiva e pronta para produção! 🎉**
