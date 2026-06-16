# 🏆 Escolha sua Versão

O projeto oferece dois caminhos, dependendo da sua necessidade de análise.

## [V1] Finance BOT (Básico)
*Foco em simplicidade e registro rápido.*
- **Arquivo**: `Finance BOT.json`
- **Fluxo**: Telegram → n8n → `gastos.csv`
- **Vantagem**: Não precisa de nada rodando além do n8n e Ollama.

## [V2] Finance BOT RAG (Avançado)
*Foco em inteligência e busca semântica.*
- **Arquivo**: `Finance BOT RAG.json`
- **Fluxo**: Telegram → n8n → API Python → ChromaDB
- **Vantagem**: Você pode fazer perguntas complexas como *"Quanto eu gastei com lazer mês passado?"* e ele buscará o contexto exato para responder.

---

## 🛠️ Comandos por Versão

| Comando | Descrição | V1 | V2 |
|----------|----------|:---:|:---:|
| `Texto Natural` | "Pizza 50 reais" | ✅ | ✅ |
| `/ver` | Últimos 10 registros | ✅ | ✅ |
| `/resumo` | Balanço por categoria | ✅ | ✅ |
| `/baixar` | Receber o CSV | ✅ | ✅ |
| `/perguntar` | IA responde com base no histórico | ❌ | ✅ |

---

## 🤖 Detalhamento dos Comandos (V2)

Na **Versão 2 (RAG)**, o bot oferece uma experiência mais rica. Abaixo está a lista exata de como os comandos respondem:

- **📝 Registrar gasto (Linguagem Natural)**: Basta escrever como você falaria.
    - *Ex: "Almoço 35 reais no crédito"*
- **📋 `/ver`**: Lista detalhada dos últimos 10 registros financeiros.
- **📊 `/resumo`**: Gera um balanço percentual e total por categoria (ex: Alimentação, Transporte).
- **📥 `/baixar`**: Envia o arquivo `gastos.csv` diretamente no chat para você abrir no Excel/Sheets.
- **🔍 `/perguntar <pergunta>`**: Consulta inteligente usando IA e sua base histórica.
    - *Ex: "/perguntar quanto gastei com uber esse mês?"*
- **💡 `/ajuda`**: Exibe o menu de comandos disponíveis e exemplos de uso.

---
[Voltar ao README](../README.md)
