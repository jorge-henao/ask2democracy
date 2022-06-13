from asyncore import read
from typing import Dict, List, Optional
#from transformers.utils.dummy_flax_objects import FlaxRobertaForMultipleChoice
import logging
import pandas as pd
from collections import OrderedDict, namedtuple
from sklearn.feature_extraction.text import TfidfVectorizer

from haystack.schema import Document
from haystack.schema import Document, MultiLabel
from haystack.nodes.base import BaseComponent
from haystack.document_stores.base import BaseDocumentStore, BaseKnowledgeGraph
from haystack.nodes.retriever import BaseRetriever
from haystack.pipelines import ExtractiveQAPipeline
from haystack.nodes import FARMReader, TransformersReader
import haystack.schema
from haystack.preprocessor.preprocessor import PreProcessor
import csv

logger = logging.getLogger(__name__)

class MockRetriever(BaseRetriever):
    
    min_doc_lenght = 100
    
    def __init__(self, top_k: int = 10, custom_query: str = None, paragraphs: List = None):
        self.top_k = top_k
        self.custom_query = custom_query
        self.paragraphs = paragraphs
            
    #Method runed by pipeline
    def retrieve(
        self, 
        query: str, 
        filters: dict = None, 
        top_k: Optional[int] = None, 
        index: str = None,
        headers: Optional[Dict[str, str]] = None) -> List[Document]:
        
        if top_k is None:
            top_k = self.top_k  
        docs = []          
        p = 1/len(self.paragraphs); i = 1
        for paragraph in self.paragraphs:
            doc_score = 1 - (p * i)
            doc = Document(content_type= "text", score= doc_score, meta= {'name': paragraph}, content = paragraph)
            docs.append(doc) 
            i = i +1
        
        return docs
        
#reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

paragraphs = ['papametro uno','papametro dos', 'papametro tres', 'papametro cuatro', 'papametro cinco', 'neo papametro']
query_str = "donde murió el buda gautama?"
wiki_retriever = MockRetriever()
results = wiki_retriever.retrieve(query = query_str, top_k = 5)

a = 1
#pipe = ExtractiveQAPipeline(reader, wiki_retriever)
#prediction = pipe.run(
#    query= query_str, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 5}}
#)

#print (prediction)