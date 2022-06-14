from typing import Optional
from fastapi import FastAPI
from repositories.proposals_commands_es_repository import ElasticCommandRepository
import config
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    #faiss_ds = FAISSDocStore(connection_string = config.FaissDSConnectionString).DBInstance()
    # query = DPRQueryCommandStack(
    #     faiss_document_store= FAISSDSCommandStack.FAISSDocStore,
    #     query_embedding_model= "IIC/dpr-spanish-question_encoder-squades-base",
    #     passage_embedding_model= "IIC/dpr-spanish-passage_encoder-squades-base",
    #     seq2seq_generator_model= "IIC/mt5-base-lfqa-es")
    #return query.execute(query = q, top_k = top_k)
    #elastic_repo = ElasticCommandRepository(elastic_endpoint = config.ElasticEndpoint)
    #elastic_repo.insert_document("docs/propuesta_viejo22.pdf")
    a = 1
    return {"message": "Hello World"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)