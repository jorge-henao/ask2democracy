from distutils.command.config import config
import uvicorn
from fastapi import FastAPI
from repositories.proposals_commands_es_repository import ProposalCommandsESRepository
from commands.proposal_command import ProposalsCommands
from config.config import Config

app = FastAPI()

@app.get("/")
def get():
    es_endpoint = Config.elastic_endpoint + "/proposals4/_doc"
    repository = ProposalCommandsESRepository(elastic_endpoint = es_endpoint, 
                                              source = "Rodolfo Hernandez")
    proposal_command = ProposalsCommands(repository = repository)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf")
    
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)