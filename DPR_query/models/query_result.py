from typing import List
from pydantic import BaseModel


class DPRSearchResult(BaseModel): 
    query: str
    results: DPRSearchResultItem 
    
class DPRSearchResultItem(BaseModel): 
    response: str
    document_id: int
    paragraph_context: str
    score: int