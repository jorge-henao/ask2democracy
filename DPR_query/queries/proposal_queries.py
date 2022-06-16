from haystack.nodes import BM25Retriever, FARMReader
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from queries.document_queries import DocumentQueries

import certifi
ca_certs=certifi.where()

class ExtractiveProposalQueries(DocumentQueries):
    
    def __init__(self, es_host: str, es_index: str, es_user, es_password, reader_name_or_path: str, use_gpu = False) -> None:
        reader = FARMReader(model_name_or_path = reader_name_or_path, use_gpu = use_gpu, num_processes=1)
        self._initialize_pipeline(es_host, es_index, es_user, es_password, reader = reader)
        
    
    def _initialize_pipeline(self, es_host, es_index, es_user, es_password, reader = None):
        if reader is not None:
            self.reader = reader
        self.es_host = es_host
        self.es_user = es_user
        self.es_password = es_password
        self.document_store = ElasticsearchDocumentStore(host = es_host, username=es_user, password=es_password, index = es_index, port = 443, scheme='https', verify_certs=True, ca_certs=ca_certs)        
        self.retriever = BM25Retriever(document_store = self.document_store)
        self.pipe = ExtractiveQAPipeline(self.reader, self.retriever)

    def search_by_query(self, query : str, retriever_top_k: int, reader_top_k: int, es_index: str = None) :
        if es_index is not None:
            self._initialize_pipeline(self.es_host, es_index, self.es_user, self.es_password)
        params = {"Retriever": {"top_k": retriever_top_k}, "Reader": {"top_k": reader_top_k}}
        prediction = self.pipe.run( query = query, params = params)      
        return prediction["answers"]
