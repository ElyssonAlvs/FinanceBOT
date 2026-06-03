# 🤖 Finance BOT - Assistente Financeiro com IA e n8n

O **Finance BOT** é um projeto de automação que transforma o Telegram em um assistente de finanças pessoais inteligente. Ele utiliza Inteligência Artificial para entender mensagens em linguagem natural, extrair dados financeiros e organizar tudo em uma planilha local.

## 🚀 Funcionalidades

### 💬 Registro por Linguagem Natural
Você não precisa preencher formulários. Basta digitar algo como:

> almoço de 35 reais no crédito

A IA identifica automaticamente:

- Valor
- Categoria
- Forma de pagamento
- Tipo de transação

### 🔒 IA Local (Privacy First)

Utiliza o **Ollama (Mistral)** rodando localmente para processar as mensagens, garantindo que seus dados não sejam enviados para APIs de terceiros.

### 📊 Gestão em CSV

Todos os gastos são salvos em um arquivo `.csv` persistente.

### 🤖 Comandos Inteligentes

| Comando | Função |
|----------|----------|
| `/resumo` | Gera um balanço dos gastos por categoria e total do mês |
| `/ver` | Mostra os últimos 10 registros |
| `/baixar` | Envia o arquivo CSV atualizado diretamente no chat |

---

## 🛠️ Tecnologias Utilizadas

- **n8n** – Orquestrador do fluxo de trabalho.
- **Ollama** – Execução local do modelo LLM (Mistral).
- **Telegram Bot API** – Interface de comunicação com o usuário.
- **ngrok** – Túnel HTTPS para ambientes self-hosted.

---

## ⚠️ Nota Importante sobre Webhooks (n8n Local vs. Desktop)

Para que o Telegram consiga enviar mensagens para o seu n8n, é necessária uma **URL pública HTTPS**.

### 🐳 n8n Self-Hosted (Docker ou npm)

O endereço `localhost:5678` não é acessível pela internet. Portanto, será necessário utilizar uma ferramenta como:

- ngrok
- Cloudflare Tunnel

Exemplo:

```bash
WEBHOOK_URL=https://seu-link-ngrok.app
```

Configure essa variável antes de iniciar o n8n.

### 💻 n8n Desktop

A versão Desktop possui um túnel integrado.

Nesse caso:

- Não é necessário instalar ngrok.
- Basta habilitar o túnel nas configurações do aplicativo.
- Os webhooks funcionarão normalmente com o Telegram.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir:

1. **n8n** instalado (Docker, npm ou Desktop);
2. **Ollama** instalado;
3. Modelo **Mistral** baixado:

```bash
ollama run mistral
```

4. Um bot criado no Telegram através do **@BotFather**;
5. **ngrok** instalado (apenas para ambientes self-hosted).

---

## 🔧 Instalação

### 1. Importar o Workflow

Clone este repositório ou baixe o arquivo:

```text
Finance BOT.json
```

No n8n:

```text
Workflows → Import from File
```

Selecione o arquivo `.json`.

### 2. Configurar Credenciais

#### Telegram Trigger / Telegram Nodes

Informe o:

```text
Bot Token
```

obtido no BotFather.

#### Ollama Chat Model

Configure o host do Ollama:

```text
http://localhost:11434
```

ou o IP correspondente ao ambiente Docker.

### 3. Configurar o Arquivo CSV

Nos nós responsáveis pela leitura e gravação do arquivo, verifique se o caminho existe.

Exemplo:

```text
/home/node/.n8n-files/gastos.csv
```

Caso necessário, altere para um diretório válido no seu sistema operacional.

### 4. Ativar o Workflow

Após concluir as configurações:

```text
Activate Workflow
```

Pronto! O bot estará operacional.

---

## 📸 Screenshots

Adicione aqui:

- Conversa com o bot no Telegram;
- Workflow completo no n8n;
- Exemplo de resumo financeiro;
- Exemplo do arquivo CSV gerado.

---

## 📂 Estrutura dos Dados

Os registros são armazenados no formato:

```csv
data,descricao,valor,categoria,forma_pagamento,tipo
2026-06-01,Almoço,35.00,alimentacao,credito,despesa
```

---

## 🎯 Objetivo

O projeto foi criado para demonstrar como integrar:

- IA Local
- Automação com n8n
- Telegram Bots
- Persistência de dados em CSV

em uma solução prática para controle financeiro pessoal.

---

## 📄 Licença

Este projeto pode ser utilizado para fins acadêmicos, educacionais e de estudo.

Desenvolvido para facilitar a vida financeira através da automação inteligente. 🚀
