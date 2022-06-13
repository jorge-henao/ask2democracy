from typing import Dict, List, Optional
from haystack.schema import Document
from transformers import (
    RagTokenizer,
    RagTokenForGeneration,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    PreTrainedTokenizer,
    BatchEncoding,
)

class BartEli5Converter:
    def __call__(
        self, tokenizer: PreTrainedTokenizer, query: str, documents: List[Document], top_k: Optional[int] = None
    ) -> BatchEncoding:
        conditioned_doc = "<P> " + " <P> ".join([d.content for d in documents])

        # concatenate question and support document into BART input
        query_and_docs = "question: {} context: {}".format(query, conditioned_doc)

        return tokenizer([(query_and_docs, "A")], truncation=True, padding=True, return_tensors="pt")