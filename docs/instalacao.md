# ⚙️ Instalação e Configuração

Siga os passos abaixo para colocar o bot para rodar no seu ambiente local.

## 1. Docker Compose (n8n)
O n8n deve rodar via Docker para facilitar o gerenciamento de arquivos. Use o arquivo abaixo:

```yaml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - /caminho/do/seu/projeto/FINANCEBOT_RAG/data:/home/node/.n8n-files
    environment:
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      - WEBHOOK_URL=https://seu-ngrok.ngrok-free.dev/
      - N8N_BLOCK_FS_WRITE_ACCESS=false
      - N8N_BLOCK_FS_READ_ACCESS=false
    restart: unless-stopped
    networks:
        - n8n-network

volumes:
  n8n_data:

networks:
  n8n-network:
```

## 2. API Python (Apenas V2)
Navegue até a pasta `FINANCEBOT_RAG` e instale as dependências:
```bash
python -m venv .venv
# Ative o venv e então:
pip install -r requirements.txt
python main.py
```

## 3. Importação do Workflow
- Importe o arquivo `Finance BOT.json` ou `Finance BOT RAG.json` no seu painel do n8n.
- Configure as credenciais do Telegram e do Ollama.

---
[Voltar ao README](../README.md)
