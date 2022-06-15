#from distutils.command.config import config
from tracemalloc import start
import uvicorn
from fastapi import FastAPI
from commands.proposal_commands import ProposalsCommands
from queries.proposal_queries import ExtractiveProposalQueries
from repositories.proposal_commands_es_repository import ProposalCommandsESRepository
from config.config import Config

app = FastAPI()

command_ropository = ProposalCommandsESRepository(es_host = Config.es_host, es_index = Config.proposals_index)
proposal_command = ProposalsCommands(repository = command_ropository)
#query = ExtractiveProposalQueries(Config.es_host, Config.proposals_index, 
#                                  Config.reader_model_name_or_path, Config.use_gpu)


@app.get("/proposals/")
def query_documents(q: str, top_k: int = 5):
    result = query.search_by_query(query = q, retriever_top_k = top_k, reader_top_k = top_k)
    return result

@app.post("/proposals/")
def add_document():
    rodolfo_pattern = "\\n[A-ZÑÁÉÍÓÚÜ0-9() \\n*]+.:\\n"
    proposal_command.insert_document(document_path = "docs/propuesta_petro22.pdf", 
                                     source = "Petro", es_index = "pretro7", start_page=8)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf",
                                      source = "Rodolfo", es_index = "rodolfo7", start_page = 12 , 
                                      titles_extract_pattern = rodolfo_pattern)
    proposal_command.insert_document(document_path = "docs/propuesta_petro22.pdf", 
                                     source = "Petro", es_index = "petrolfo7", start_page=8)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf",
                                      source = "Rodolfo", es_index = "petrolfo7", start_page = 12 , 
                                      titles_extract_pattern = rodolfo_pattern)
    
    return {"message": "Documents added"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)