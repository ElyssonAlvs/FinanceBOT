import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.indexer import Indexer
from src.retriever import Retriever

logger = logging.getLogger(__name__)
# Configuração via variáveis de ambiente para facilitar Windows vs WSL
# Exemplo no Windows: C:\Users\elyss\Desktop\Projects\FinanceBOT\data\gastos.csv
DATA_SOURCE = os.getenv("DATA_SOURCE_PATH", r"C:\Users\elyss\Desktop\Projects\FinanceBOT\FINANCEBOT_RAG\data\gastos.csv")
logger.info(f"DATA_SOURCE ativo: {DATA_SOURCE}")
CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da API.
    Inicializa os modelos de ML uma única vez.
    """
    logger.info("Iniciando modelos de IA (FinanceBOT V2)...")
    try:
        app.state.indexer = Indexer(db_path=CHROMA_PATH)
        app.state.retriever = Retriever(db_path=CHROMA_PATH)
        logger.info("Modelos inicializados com sucesso.")
    except Exception:
        logger.exception("Falha crítica ao inicializar modelos no startup")
    
    yield
    
    logger.info("Encerrando API e limpando memória...")

app = FastAPI(title="FinanceBOT RAG API v2", lifespan=lifespan)

class SearchQuery(BaseModel):
    query: str
    n_results: int = 5

@app.post("/index")
async def index_data(filepath: str = DATA_SOURCE):
    """
    Indexa os dados do arquivo CSV no banco vetorial.
    Pode receber um caminho customizado (ex: caminho WSL).
    """
    indexer = getattr(app.state, "indexer", None)
    if not indexer:
        raise HTTPException(status_code=503, detail="Serviço de indexação não disponível.")
        
    try:
        logger.info(f"Iniciando indexação do arquivo: {filepath}")
        count = indexer.index_csv(filepath)
        return {"message": f"Sucesso! {count} itens indexados de {filepath}"}
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {filepath}")
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado.")
    except Exception:
        logger.exception("Erro durante o processo de indexação")
        raise HTTPException(status_code=500, detail="Erro interno ao indexar dados.")

@app.post("/search")
async def search(search_query: SearchQuery):
    """
    Busca os gastos mais relevantes (RAG) para responder uma pergunta.
    """
    retriever = getattr(app.state, "retriever", None)
    if not retriever:
        raise HTTPException(status_code=503, detail="Serviço de busca não disponível.")

    try:
        results = retriever.search(search_query.query, n_results=search_query.n_results)
        return {"query": search_query.query, "results": results}
    except Exception:
        logger.exception("Erro ao realizar busca semântica")
        raise HTTPException(status_code=500, detail="Erro interno ao realizar busca.")

@app.get("/health")
async def health():
    """Verifica saúde do sistema e conexão com banco de dados."""
    retriever = getattr(app.state, "retriever", None)
    size = 0
    if retriever:
        try:
            size = retriever.collection.count()
        except: pass
    
    return {
        "status": "online",
        "database_size": size,
        "data_source": DATA_SOURCE
    }

@app.get("/analytics")
async def get_analytics(filepath: str = DATA_SOURCE):
    """
    Retorna estatísticas consolidadas dos gastos.
    """
    if not Path(filepath).exists():
        raise HTTPException(status_code=404, detail="Arquivo de dados não encontrado.")
    
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            return {"total_gasto": 0, "por_categoria": {}, "maior_gasto": None, "gasto_mes_atual": 0}

        # Garantir colunas básicas
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)
        
        if 'tipo' not in df.columns:
            df['tipo'] = 'despesa'
        else:
            df['tipo'] = df['tipo'].astype(str).str.strip().str.lower()

        # Normalizar categorias
        if 'categoria' in df.columns:
            df['categoria'] = df['categoria'].astype(str).str.lower().str.strip()
            df['categoria'] = df['categoria'].replace({
                'alimentação': 'alimentacao', 'saúde': 'saude',
                'entretenimento': 'lazer', 'educação': 'educacao'
            })

        # Filtrar apenas despesas
        despesas = df[df['tipo'] != 'receita'].copy()
        
        # Cálculo de gasto do mês atual
        from datetime import datetime
        agora = datetime.now()
        mes_atual_str = agora.strftime("%Y-%m")
        
        despesas['mes'] = despesas['data'].astype(str).str.slice(0, 7)
        gasto_mes_atual = float(despesas[despesas['mes'] == mes_atual_str]['valor'].sum())
        
        total_gasto = float(despesas['valor'].sum())
        por_categoria = despesas.groupby('categoria')['valor'].sum().to_dict()
        
        maior_item = despesas.loc[despesas['valor'].idxmax()] if not despesas.empty else None
        maior_gasto = {
            "descricao": maior_item['descricao'],
            "valor": float(maior_item['valor']),
            "data": maior_item['data']
        } if maior_item is not None else None

        return {
            "total_gasto": total_gasto,
            "gasto_mes_atual": gasto_mes_atual,
            "mes_referencia": mes_atual_str,
            "por_categoria": por_categoria,
            "maior_gasto": maior_gasto,
            "total_registros": len(df)
        }
    except Exception as e:
        logger.exception("Erro ao gerar analytics")
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")

@app.get("/recent")
async def get_recent(filepath: str = DATA_SOURCE, limit: int = 10):
    """
    Retorna os últimos registros do arquivo.
    """
    if not Path(filepath).exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            return {"count": 0, "items": []}
        
        # Pega os últimos registros (limit)
        recent = df.tail(limit).iloc[::-1] # Inverte para mostrar do mais novo para o mais velho
        items = recent.to_dict(orient='records')
        
        return {"count": len(items), "items": items}
    except Exception as e:
        logger.exception("Erro ao buscar registros recentes")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
