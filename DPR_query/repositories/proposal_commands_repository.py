from abc import ABC, abstractmethod

class DocumentCommandsRepository(ABC):
    
    @abstractmethod
    def insert_document(self, document_path, source, es_index, titles_extract_pattern = None):
        pass
    
    @abstractmethod
    def _preproces_documents(self, document_path, source, es_index, start_page, titles_extract_pattern):
        pass
    
    @abstractmethod
    def get_elastic_endpoint(self):
        pass
