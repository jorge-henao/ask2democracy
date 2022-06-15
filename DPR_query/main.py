#from distutils.command.config import config
import uvicorn
from fastapi import FastAPI
from queries.extractive_proposal_queries import ExtractiveProposalQueries
from commands.proposal_command import ProposalsCommands
from repositories.proposal_commands_es_repository import ProposalCommandsESRepository
from config.config import Config

app = FastAPI()

@app.get("/proposals/")
def query_documents(q: str, top_k: int = 5):
    query = ExtractiveProposalQueries(Config.es_host, Config.proposals_index,
                                      Config.reader_model_name_or_path, Config.use_gpu)
    result = query.search_by_query(query = q, retriever_top_k = top_k, reader_top_k = top_k)
    return {"message": "Hello World"}

@app.post("/proposals/")
def add_document():
    repository = ProposalCommandsESRepository(es_host = Config.es_host, index = Config.proposals_index,
                                              source = "Rodolfo Hernandez")
    proposal_command = ProposalsCommands(repository = repository)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf")
    
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)