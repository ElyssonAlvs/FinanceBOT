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
[Voltar ao README](../README.md)
