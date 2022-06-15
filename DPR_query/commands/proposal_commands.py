from multiprocessing import parent_process
from repositories.proposal_commands_es_repository import DocumentCommandsRepository

class ProposalsCommands():
    
    def __init__(self, repository: DocumentCommandsRepository ) -> None:
        self.repository = repository
        pass
    
    def insert_document(self, document_path, source, titles_extract_pattern = None):
        self.repository.insert_document(document_path, source, titles_extract_pattern)