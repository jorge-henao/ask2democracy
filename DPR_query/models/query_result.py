from typing import List
from pydantic import BaseModel


class SearchResult(BaseModel): 
    query: str
    results: DPRSearchResultItem 
    
class SearchResultItem(BaseModel): 
    response: str
    document_id: int
    paragraph_context: str
    score: int