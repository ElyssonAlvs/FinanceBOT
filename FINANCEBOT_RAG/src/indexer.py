import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import hashlib
from typing import List, Dict
import os

class Indexer:
    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "gastos"):
        # Garante que o diretório do banco exista
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            
        self.client = chromadb.PersistentClient(path=db_path)
        # Modelo multilingue local para os embeddings
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_fn
        )

    def generate_id(self, row: pd.Series) -> str:
        """Gera um ID único baseado nos dados da linha para evitar duplicatas."""
        content = f"{row['data']}-{row['descricao']}-{row['valor']}"
        return hashlib.md5(content.encode()).hexdigest()

    def serialize_row(self, row: pd.Series) -> str:
        """Transforma uma linha do CSV em texto para o modelo de IA."""
        return f"Gasto de R${row['valor']} em {row['data']} para {row['descricao']} na categoria {row['categoria']}."

    def index_csv(self, file_path: str):
        """Lê o CSV, limpa a coleção antiga e indexa os dados atuais."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Limpa a coleção para evitar "memórias" de dados deletados ou corrigidos
        count_before = self.collection.count()
        if count_before > 0:
            # Pegamos todos os IDs e deletamos
            all_ids = self.collection.get()['ids']
            if all_ids:
                self.collection.delete(ids=all_ids)
            logger.info(f"Coleção limpa. {count_before} registros antigos removidos.")

        documents = []
        metadatas = []
        ids = []

        for _, row in df.iterrows():
            doc = self.serialize_row(row)
            # Geramos um ID baseado no conteúdo se o CSV não tiver ID fixo
            doc_id = str(row['id']) if 'id' in row else self.generate_id(row)
            
            documents.append(doc)
            metadatas.append(row.to_dict())
            ids.append(doc_id)

        # Upsert: Insere novos ou atualiza se o ID já existir
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return len(ids)

if __name__ == "__main__":
    # Exemplo de uso com caminho WSL
    WSL_PATH = r"\home\elyss\n8n\data\gastos.csv"
    indexer = Indexer()
    try:
        count = indexer.index_csv(WSL_PATH)
        print(f"Sucesso! {count} registros processados.")
    except Exception as e:
        print(f"Erro: {e}")
