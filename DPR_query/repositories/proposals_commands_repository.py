from abc import ABC, abstractmethod

class DocumentCommandsRepository(ABC):
    
    @abstractmethod
    def insert_document(self, document_path):
        pass
    
    @abstractmethod
    def preproces_documents(self, document_path):
        pass
