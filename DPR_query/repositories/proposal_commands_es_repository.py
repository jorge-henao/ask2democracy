from multiprocessing import parent_process
from operator import index
import re
import uuid
import json
import datetime
import requests
import fitz
from base64 import b64encode
from repositories.proposal_commands_repository import DocumentCommandsRepository

        
class ProposalCommandsESRepository(DocumentCommandsRepository):
    
    def __init__(self, es_host, es_index, es_user, es_password) -> None:
        self.es_host = es_host
        self.es_index = es_index
        self.__set_elastic_endpoint(es_host, es_index)
        self.error_file = open('./errorwikioutput.txt','w+')
        credentials = f"{es_user}:{es_password}"
        self.credentials = b64encode(b"elastic:siKAHmmk2flwEaKNqQVZwp49").decode("ascii")
        self.auth_header = { 'Authorization' : 'Basic %s' %  self.credentials }
    
    def __set_elastic_endpoint(self, es_host, es_index):
        self.es_host = es_host
        self.es_index = es_index
    
    def get_elastic_endpoint(self):
        return f"https://{self.es_host}:443/{self.es_index}/_doc"
    
    def insert_document(self, document_path, source, es_index = None, start_page = 0, extract_paragraph_pattern = None):
        if es_index is not None:
            self.__set_elastic_endpoint(self.es_host, es_index)
        paragraphs = self._preproces_documents(document_path, source, start_page, extract_paragraph_pattern)
        self.__upload_paragraphs_to_cluster(paragraphs= paragraphs, source = source)
     
    def _preproces_documents(self, document_path, source, start_page, extract_paragraph_pattern):
        if extract_paragraph_pattern is None:
            paragraphs = self.__extract_pages_from_document(document_path, source = source, start_page = start_page)
        else: 
            paragraphs = self.__extract_paragraphs_from_document(document_path, source, extract_paragraph_pattern, start_page)
        
        return paragraphs
    
    def __extract_paragraphs_from_document(self, document_path, source, pattern, start_page = 0):
        paragraphs = []
        try:
            current_title = ""
            with fitz.open(document_path) as doc:
                i = 0
                for page in doc:
                    if i < start_page : i += 1; continue
                    text = page.get_text()
                    title = re.findall(pattern = pattern, string = text)
                    if len(title) > 0:
                        current_title = title[0].replace('\n','').replace('  ','-').replace(' ','').replace('-',' ').capitalize()
                        current_title = f"{source} {current_title}"
                    text = f"{current_title}\\n{text}"
                    paragraphs.append({"title": current_title, "text" : text})
                    i += 1
                return paragraphs
        except Exception as ex:
            #self.error_file.write(title + str(len(text)) + ':' + str(ex) + '\\n')
            return paragraphs
        
    def __extract_pages_from_document(self, document_path, source, start_page = 0):
        paragraphs = []
        try:
            i =0
            with fitz.open(document_path) as doc:
                for page in doc:
                    if i < start_page : i += 1; continue
                    text = page.get_text()
                    text = f"{source}\\n{text}"
                    paragraphs.append({"title": source, "text" : text})
                    i += 1
                return paragraphs
        except Exception as ex:
            #self.error_file.write(title + str(len(text)) + ':' + str(ex) + '\\n')
            return paragraphs
    
    def __upload_paragraphs_to_cluster(self, paragraphs, source):
        p_index = 0
        for paragraph in paragraphs:
            title = paragraph['title']
            text = paragraph['text']  
            doc_id = str(uuid.uuid4())
            self.__upload_paragraph(title, text, p_index, doc_id, source)    
            p_index += 1
            
    def __upload_paragraph (self, title, p_content, p_index, doc_id, source):
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

        r = requests.post(self.get_elastic_endpoint(), json = post_data, headers = self.auth_header)
        print(r.text)      