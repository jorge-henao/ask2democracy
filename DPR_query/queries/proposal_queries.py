from haystack.nodes import BM25Retriever, FARMReader
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from queries.document_queries import DocumentQueries

class ExtractiveProposalQueries(DocumentQueries):
    
    def __init__(self, es_host: str, index: str, reader_name_or_path: str, use_gpu = False) -> None:
        self.document_store = ElasticsearchDocumentStore(host = es_host, username="", password="", index = index)        
        self.retriever = BM25Retriever(document_store = self.document_store)
        self.reader = FARMReader(model_name_or_path = reader_name_or_path, use_gpu = use_gpu, num_processes=2)
        self.pipe = ExtractiveQAPipeline(self.reader, self.retriever)
        
    def search_by_query(self, query : str, retriever_top_k: int, reader_top_k: int):
        params = {"Retriever": {"top_k": retriever_top_k}, "Reader": {"top_k": reader_top_k}}
        prediction = self.pipe.run( query = query, params = params)      
        return prediction["answers"]
