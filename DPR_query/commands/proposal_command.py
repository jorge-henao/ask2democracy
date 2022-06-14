from multiprocessing import parent_process
from repositories.proposals_commands_es_repository import DocumentCommandsRepository

class ProposalsCommands():
    
    def __init__(self, repository: DocumentCommandsRepository ) -> None:
        self.repository = repository
        pass
    
    def insert_document(self, document_path):
        self.repository.insert_document(document_path)