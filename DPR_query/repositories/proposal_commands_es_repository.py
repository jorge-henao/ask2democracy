from multiprocessing import parent_process
import re
import uuid
import json
import datetime
import requests
import fitz

from repositories.proposal_commands_repository import DocumentCommandsRepository

class ProposalCommandsESRepository(DocumentCommandsRepository):
    
    def __init__(self, es_host, es_index, source) -> None:
        self.elastic_endpoint =  f"http://{es_host}:9200/{es_index}/_doc"
        self.source = source
        self.error_file = open('./errorwikioutput.txt','w+')
    
    def insert_document(self, document_path):
        paragraphs = self.preproces_documents(document_path)
        self.upload_paragraphs_to_cluster(paragraphs= paragraphs, source = self.source)
     
    def preproces_documents(self, document_path):
        paragraphs = self.extract_paragraphs_from_document(document_path)
        return paragraphs
    
    def extract_paragraphs_from_document(self, document_path):
        paragraphs = []
        try:
            pattern = "\\n[A-ZÑÁÉÍÓÚÜ0-9() \\n*]+.:\\n"
            current_title = ""
            with fitz.open(document_path) as doc:
                for page in doc:
                    text = page.get_text()
                    title = re.findall(pattern = pattern, string = text)
                    if len(title) > 0:
                        current_title = title[0].replace('\n','').replace('  ','-').replace(' ','').replace('-',' ').capitalize()
                        current_title = f"{self.source} {current_title}"
                        text = f"{current_title}\\n{text}"
                        paragraphs.append({"title": current_title, "text" : text})
                return paragraphs
        except Exception as ex:
            #self.error_file.write(title + str(len(text)) + ':' + str(ex) + '\\n')
            return paragraphs
    
    def upload_paragraphs_to_cluster(self, paragraphs, source):
        p_index = 0
        for paragraph in paragraphs:
            title = paragraph['title']
            text = paragraph['text']  
            doc_id = str(uuid.uuid4())
            self.upload_paragraph(title, text, p_index, doc_id, source)    
            p_index += 1
            
    def upload_paragraph (self, title, p_content, p_index, doc_id, source):
        created_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        post_data  = {
            "document_id": doc_id,
            "content" : p_content,
            "paragraph_index": p_index,
            "createdDate": {
                "date" : created_date
            },
            "source": source,
            "name": title,
            "title": title
        }

        r = requests.post(self.elastic_endpoint, json = post_data)
        print(r.text)      