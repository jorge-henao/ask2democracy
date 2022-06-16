from abc import ABC, abstractmethod

class DocumentQueries(ABC):
    
    @abstractmethod
    def search_by_query(self, query : str, retriever_top_k: int, reader_top_k: int, es_index: str):
        pass