# 🤖 Finance BOT - Guia de Documentação

Bem-vindo ao repositório do **Finance BOT**. Este projeto utiliza IA local (Ollama) e n8n para transformar o Telegram em seu assistente financeiro pessoal.

## 📑 Documentação Rápida

Para facilitar a navegação, dividimos o guia em tópicos didáticos:

1.  **[Como o Projeto Funciona](./docs/funcionamento.md)**: Entenda a arquitetura entre Telegram, n8n e a API Python.
2.  **[Instalação e Configuração](./docs/instalacao.md)**: Guia passo a passo para rodar o Docker e a API.
3.  **[Diferenças entre V1 e V2](./docs/versões.md)**: Escolha entre a versão simples em CSV ou a avançada com RAG (Busca Semântica).

---

## 🚀 Início Rápido (TL;DR)

- **V1 (Básico)**: Use o arquivo `Finance BOT.json`. Salva tudo direto no CSV.
- **V2 (RAG)**: Use o arquivo `Finance BOT RAG.json`. Requer a API Python rodando para responder perguntas complexas via `/perguntar`.

---

## 🔒 Segurança de Dados
Este projeto ignora automaticamente seus arquivos de dados (`gastos.csv`) e pastas de banco de dados (`chroma_db/`). Sinta-se seguro para fazer commits; seus dados financeiros permanecerão apenas na sua máquina local.

---
*Desenvolvido para automação pessoal e estudos de IA.*
