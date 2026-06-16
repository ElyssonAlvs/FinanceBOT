# Finance BOT API 🚀

API baseada em FastAPI para busca semântica (RAG) e análise de dados financeiros.

## 🚀 Como Executar

### Pré-requisitos
*   [Python 3.12+](https://www.python.org/)
*   [uv](https://github.com/astral-sh/uv)

### Instalação e Execução
```bash
# Instalar dependências
uv sync

# Iniciar o servidor
uv run python main.py
```
A API estará disponível em `http://localhost:8000`.

---

## 📡 Referência da API

### 1. Indexação
Alimenta o banco de dados vetorial com os dados do CSV.

*   **Rota:** `/index`
*   **Método:** `POST`
*   **Query Params:** `filename` (Opcional, padrão: `gastos.csv`)
*   **Resposta:** `{"message": "Successfully indexed X items from gastos.csv"}`

### 2. Busca Semântica (RAG)
Recupera os gastos mais relevantes baseados no significado da pergunta.

*   **Rota:** `/search`
*   **Método:** `POST`
*   **Corpo (JSON):**
    ```json
    {
      "query": "gastos com alimentação",
      "n_results": 3
    }
    ```
*   **Resposta:** Contém a pergunta original e uma lista de resultados com `score_normalized` (0 a 1).

### 3. Analytics
Agrega dados financeiros (somas e totais) que o RAG não processa.

*   **Rota:** `/analytics`
*   **Método:** `GET`
*   **Resposta:**
    ```json
    {
      "total_gasto": 1500.00,
      "por_categoria": { "Alimentação": 500.0, "Transporte": 1000.0 },
      "maior_gasto": { ... }
    }
    ```

### 4. Health Check
Verifica o status da API e o tamanho da coleção indexada.

*   **Rota:** `/health`
*   **Método:** `GET`
*   **Resposta:** `{"status": "ok", "collection_size": 10, "search_ready": true}`

---

## 📂 Estrutura de Arquivos

*   `main.py`: Ponto de entrada e definição das rotas FastAPI.
*   `src/indexer.py`: Processamento de CSV e carga no ChromaDB.
*   `src/retriever.py`: Busca vetorial, Reranking e Normalização.
*   `data/gastos.csv`: Fonte de dados bruta.
*   `chroma_db/`: Persistência do banco de dados vetorial.
