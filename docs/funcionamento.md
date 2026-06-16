# 🧠 Como o Projeto Funciona

O **Finance BOT** é um ecossistema que integra o Telegram ao seu controle financeiro usando Inteligência Artificial. Ele opera em três camadas principais:

## 1. Interface (Telegram)
O usuário interage com um Bot do Telegram. As mensagens podem ser:
- **Linguagem Natural**: "Almoço 35 reais no crédito".
- **Comandos**: `/ver`, `/resumo`, `/baixar`, `/perguntar`.

## 2. Orquestração (n8n)
O n8n atua como o cérebro, recebendo os Webhooks do Telegram e decidindo o que fazer:
- **Extração**: Usa IA (Ollama/Mistral) para converter texto em dados estruturados (JSON).
- **Persistência**: Grava os dados estruturados no arquivo `gastos.csv`.
- **RAG (V2)**: Se for uma pergunta, ele consulta a API Python para buscar informações contextuais.

## 3. Inteligência e Dados (Python & ChromaDB - V2)
Na versão avançada, uma API FastAPI gerencia a "memória" do bot:
- **Indexer**: Lê o `gastos.csv` e transforma cada linha em um "vetor" (números que representam o significado).
- **Vector Database (ChromaDB)**: Armazena esses vetores.
- **Retriever**: Quando você pergunta algo, o bot busca os registros mais parecidos semanticamente para formular a resposta.

---
[Voltar ao README](../README.md)
