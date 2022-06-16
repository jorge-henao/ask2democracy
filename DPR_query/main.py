#from distutils.command.config import config
from distutils.command.config import config
from tracemalloc import start
import uvicorn
from fastapi import FastAPI
from commands.proposal_commands import ProposalsCommands
from queries.proposal_queries import ExtractiveProposalQueries
from repositories.proposal_commands_es_repository import ProposalCommandsESRepository
from config.config import Config

app = FastAPI()

# command_ropository = ProposalCommandsESRepository(es_host = Config.es_host, es_index = Config.proposals_index, 
#                                                   es_user = Config.es_user, es_password = Config.es_password)
# proposal_command = ProposalsCommands(repository = command_ropository)
query = ExtractiveProposalQueries(es_host = Config.es_host, es_index = Config.proposals_index,
                                  es_user = Config.es_user, es_password = Config.es_password,
                                  reader_name_or_path = Config.reader_model_name_or_path,
                                  use_gpu = Config.use_gpu)

@app.get("/proposals/")
def query_documents(q: str, retriever_top_k: int = 3, reader_top_k: int = 1):
    #result = query.search_by_query(query = q, retriever_top_k = retriever_top_k, reader_top_k = reader_top_k, es_index = "petro9")
    #result += query.search_by_query(query = q, retriever_top_k = retriever_top_k, reader_top_k = reader_top_k, es_index = "rodolfo9")
    result = query.search_by_query(query = q, retriever_top_k = retriever_top_k, reader_top_k = reader_top_k, es_index = "petrolfo")

    return result

@app.post("/proposals/")
def add_document():
    rodolfo_pattern = "\\n[A-ZÑÁÉÍÓÚÜ0-9() \\n*]+.:\\n"
    proposal_command.insert_document(document_path = "docs/propuesta_petro22.pdf", 
                                     source = "Petro", es_index = "petro", start_page=8)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf",
                                      source = "Rodolfo", es_index = "rodolfo", start_page = 12 , 
                                      titles_extract_pattern = rodolfo_pattern)
    proposal_command.insert_document(document_path = "docs/propuesta_petro22.pdf", 
                                     source = "Petro", es_index = "petrolfo", start_page=8)
    proposal_command.insert_document(document_path = "docs/propuesta_rodolfo_hernandez22.pdf",
                                      source = "Rodolfo", es_index = "petrolfo", start_page = 12 , 
                                      titles_extract_pattern = rodolfo_pattern)
    
    return {"message": "Documents added"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)                                                                                                                                                                                            