from distutils.command.config import config
import uvicorn
from fastapi import FastAPI
from commands.elastic_command_repository import ESCommandRepository
from config.config import Config

app = FastAPI()

@app.get("/")
def get():
    es_endpoint = Config.elastic_endpoint + "/proposals/_doc"
    repo = ESCommandRepository(elastic_endpoint = es_endpoint)
    repo.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf")

    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)