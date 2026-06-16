import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.indexer import Indexer
from src.retriever import Retriever

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuração via variáveis de ambiente
DATA_SOURCE = os.getenv("DATA_SOURCE_PATH", r"C:\Users\elyss\Desktop\Projects\FinanceBOT\FINANCEBOT_RAG\data\gastos.csv")
CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

def safe_float(val):
    """Garante que o valor seja um float compatível com JSON (não-NaN)."""
    try:
        f = float(val)
        return f if not (np.isnan(f) or np.isinf(f)) else 0.0
    except:
        return 0.0

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da API."""
    logger.info("Iniciando modelos de IA (FinanceBOT V2)...")
    try:
        app.state.indexer = Indexer(db_path=CHROMA_PATH)
        app.state.retriever = Retriever(db_path=CHROMA_PATH)
        logger.info("Modelos inicializados com sucesso.")
    except Exception:
        logger.exception("Falha crítica ao inicializar modelos no startup")
    yield
    logger.info("Encerrando API...")

app = FastAPI(title="FinanceBOT RAG API v2", lifespan=lifespan)

class SearchQuery(BaseModel):
    query: str
    n_results: int = 5

@app.post("/index")
async def index_data(filepath: str = DATA_SOURCE):
    indexer = getattr(app.state, "indexer", None)
    if not indexer:
        raise HTTPException(status_code=503, detail="Serviço de indexação não disponível.")
    try:
        count = indexer.index_csv(filepath)
        return {"message": f"Sucesso! {count} itens indexados"}
    except Exception as e:
        logger.exception("Erro ao indexar")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search(search_query: SearchQuery):
    retriever = getattr(app.state, "retriever", None)
    if not retriever:
        raise HTTPException(status_code=503, detail="Serviço de busca não disponível.")
    try:
        results = retriever.search(search_query.query, n_results=search_query.n_results)
        return {"query": search_query.query, "results": results}
    except Exception as e:
        logger.exception("Erro na busca")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics(filepath: str = DATA_SOURCE):
    if not Path(filepath).exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        if df.empty:
            return {"total_gasto": 0, "por_categoria": {}, "maior_gasto": None, "recent_items": []}

        # Normalização rigorosa
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0.0)
        df['tipo'] = df.get('tipo', 'despesa').astype(str).str.strip().str.lower()
        df['categoria'] = df.get('categoria', 'outros').astype(str).str.lower().str.strip()
        df['descricao'] = df.get('descricao', '').fillna("").astype(str)
        df['data'] = df.get('data', '').fillna("").astype(str)

        despesas = df[df['tipo'] != 'receita'].copy()
        mes_atual = datetime.now().strftime("%Y-%m")
        
        # Consolidação segura para JSON
        total_gasto = safe_float(despesas['valor'].sum())
        gasto_mes_atual = safe_float(despesas[despesas['data'].str.contains(mes_atual, na=False)]['valor'].sum())
        
        cat_sums = despesas.groupby('categoria')['valor'].sum().to_dict()
        por_categoria = {str(k): safe_float(v) for k, v in cat_sums.items()}

        maior_gasto = None
        if not despesas.empty:
            item = despesas.loc[despesas['valor'].idxmax()]
            maior_gasto = {
                "descricao": str(item['descricao']),
                "valor": safe_float(item['valor']),
                "data": str(item['data'])
            }

        # Itens recentes (limpeza final de NaNs para evitar erro 500)
        recent_df = df.tail(5).iloc[::-1].copy()
        for col in recent_df.columns:
            if recent_df[col].dtype == 'float64' or recent_df[col].dtype == 'int64':
                recent_df[col] = recent_df[col].apply(safe_float)
            else:
                recent_df[col] = recent_df[col].fillna("")
        
        return {
            "total_gasto": total_gasto,
            "gasto_mes_atual": gasto_mes_atual,
            "mes_referencia": mes_atual,
            "por_categoria": por_categoria,
            "maior_gasto": maior_gasto,
            "recent_items": recent_df.to_dict(orient='records'),
            "total_registros": int(len(df))
        }
    except Exception as e:
        logger.exception("Erro no analytics")
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
