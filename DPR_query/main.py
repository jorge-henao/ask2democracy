from typing import Optional
from fastapi import FastAPI
from db import dpr_query_stack

app = FastAPI()

@app.get("/documents")
def query_docs(q: str, top_k: int):
    faiss_ds = FAISSDocStore(connection_string = config.FaissDSConnectionString).DBInstance()
    query = DPRQueryCommandStack(
        faiss_document_store= FAISSDSCommandStack.FAISSDocStore,
        query_embedding_model= "IIC/dpr-spanish-question_encoder-squades-base",
        passage_embedding_model= "IIC/dpr-spanish-passage_encoder-squades-base",
        seq2seq_generator_model= "IIC/mt5-base-lfqa-es")
    return query.execute(query = q, top_k = top_k)