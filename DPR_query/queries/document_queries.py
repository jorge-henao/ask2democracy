from abc import ABC, abstractmethod

class DocumentQueries(ABC):
    
    @abstractmethod
    def search_by_query(self, query: str, top_k: int):
        pass