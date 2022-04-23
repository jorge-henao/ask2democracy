import os
import csv
from fileinput import filename
from haystack.nodes import PDFToTextConverter, PreProcessor

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
        
build_docs_csv("/docs","propuestas_presidenciales_col_22.csv")