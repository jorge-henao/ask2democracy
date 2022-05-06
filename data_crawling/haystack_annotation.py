import os
from typing import List
import csv
from fileinput import filename
from filelock import WindowsFileLock
from haystack.nodes import PDFToTextConverter, PreProcessor
import fitz
import uuid
import json

def build_docs_csv(directory, out_csv_name):  
    out_csv = open(out_csv_name, 'a')
    out_csv_header = ['document_text','document_identifier','order']
    writer = csv.writer(out_csv)  
    writer.writerow(out_csv_header)
    converter = PDFToTextConverter(remove_numeric_tables = True, valid_languages=["es"])
    for file_name in os.listdir(directory):
        if not file_name.lower.endswith("pdf") : continue
        file_path = os.path.join(directory, file_name)
        pdf_text = converter.convert(file_path = file_path, meta = None)
        data = [pdf_text, file_name, ""]
        writer.writerow(data)
        
def build_questions_csv(raw_questions_file: str,  out_csv_name: str, document_id: int, candidatos: List):  
    out_csv = open(out_csv_name, 'w')
    out_csv_header = ['question']
    writer = csv.writer(out_csv)  
    writer.writerow(out_csv_header)
    
    with open(raw_questions_file) as qf:
        lines = qf.readlines()
        for line in lines:
            final_questions = [line.replace("[CANDIDATO]", c).strip() for c in candidatos]
            for question in final_questions:
                writer.writerow([question])
      
def build_txt_from_pdf(pdf_path_file: str, out_txt_name: str):  
    final_text = ""
    with fitz.open(pdf_path_file) as doc:
        for page in doc:
            text = page.get_text()
            final_text = final_text + text
            print(text) 

    with open(out_txt_name, 'w', encoding='utf-8') as f:
        f.write(final_text)

def build_docs_csv_from_pdf(pdf_path_file: str, out_file_name: str):  
    with open(out_file_name, 'w') as out_csv:
        out_csv_header = ['document_text','document_identifier','order']
        writer = csv.writer(out_csv)
        writer.writerow(out_csv_header)
        i = 1; doc_id = str(uuid.uuid4())
        with fitz.open(pdf_path_file) as doc:
            for page in doc:
                text = page.get_text()
                if text.strip() == "": continue
                writer.writerow([text, doc_id, i])
                i = i + 1

#build_txt_from_pdf("docs/Fajardo22.pdf","Fajardo22.txt")
#build_docs_csv("/docs","propuestas_presidenciales_col_22.csv")
#build_questions_csv("raw_questions.txt",
#                   out_csv_name="docs/questions_fajardo.csv",
#                   document_id=566783,
#                   candidatos=["Fajardo"])

def rebuild_squad_context_from_paged_csv(squad_file_path, csv_context_file_path, out_squad_file_name):
    squad_dict = json.loads(open(squad_file_path).read())    
    with open(csv_context_file_path) as f:
        docs_dict = [{k: v for k, v in row.items()}
                     for row in csv.DictReader(f, skipinitialspace=True)]
    paragraphs = []
    for question in squad_dict['data'][0]['paragraphs'][0]['qas']:
        question_answers = question['answers']
        for answer in question_answers:
            answer_text = answer['text'] if 'Fico' in question else answer['text'].replace('\n',' \n')
            context = {i: docs_dict[i]['document_text']
                    for i in range(len(docs_dict)) 
                    if docs_dict[i]['document_text'].find(answer_text) != -1}
            if len(context) < 1: continue
            context = list(context.values())[0]
            answer_start = context.index(answer_text)
            answer_end = answer_start + len(answer_text)
            question =  {
                "question" : question['question'],
                "question_id" :question['id'],
                "answers" : [{
                    "answer_id": answer["answer_id"],
                    "document_id": answer["document_id"],
                    "question_id": answer["question_id"],
                    "text": answer_text,
                    "answer_start": answer_start,
                    "answer_end": answer_end,
                    "answer_category": None
                }],
                "is_impossible": False
            }
            paragraph = {
                "qas": [question],
                "context": context
            }
            paragraphs.append(paragraph)
    squad_data = {
        "data": [{
            "paragraphs": paragraphs
            }]
        }
    with open(out_squad_file_name,'w', encoding='utf-8') as f:
        f.write(json.dumps(squad_data, ensure_ascii=False))
            
#rebuild_squad_context_from_paged_csv("dataset/squad_fico_fajardo.json","docs/propuesta_fajardo22.csv","squad_fajardo.json")
rebuild_squad_context_from_paged_csv("dataset/squad_fico_fajardo.json","docs/propuesta_fico22.csv","squad_fico.json")
#build_docs_csv_from_pdf("docs/fico22.pdf", "docs/docs_fico3.csv")
#build_txt_from_pdf("docs/fico22.pdf", "docs/fico22_2.txt")
#TODO: corregir disparidad en documentos de fico , el del sistema de anotación está diferente al del squad.
#basarse en texto fico22, hacerle cirugía manual . ¿porqué estan diferentes?
#caso  Triplicar la cobertura de Jóvenes en Acción: Pasaremos a 1.200,000 
#"beneficiarios, hoy alcanzan los 400.000.
#¿Cómo Fico promoverá el mercado laboral de los jóvenes?
#TODO: soportar a multiples candidatos al hacer rebuild