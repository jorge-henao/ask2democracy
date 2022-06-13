from haystack.utils import print_documents
from haystack.pipelines import DocumentSearchPipeline
from haystack.nodes import DensePassageRetriever
from haystack.document_stores import FAISSDocumentStore
from haystack.nodes import Seq2SeqGenerator
from core import bart_eli5_converter

class DPRQueryCommandStack():
    
    def __init__(self, faiss_document_store : FAISSDocumentStore, 
                 query_embedding_model : str, passage_embedding_model: str,
                 seq2seq_generator_model: str) -> None:
        self.query_embedding_model = query_embedding_model,
        self.passage_embedding_model = passage_embedding_model
        self.retriever = DensePassageRetriever(
            document_store = faiss_document_store,
            query_embedding_model = query_embedding_model,
            passage_embedding_model = passage_embedding_model
        )
        self.generator = Seq2SeqGenerator(
            model_name_or_path = seq2seq_generator_model, 
            input_converter = BartEli5Converter()) 
        self.generative_pipe = GenerativeQAPipeline(
            self.generator, self.retriever)        
        
    def execute(query : str, top_k: int):
        results = generative_pipe.run(query= query, params={"Retriever": {"top_k": top_k}}
        return results                          
)