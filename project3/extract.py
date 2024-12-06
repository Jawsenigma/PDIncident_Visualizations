import os
import re
from pypdf import PdfReader

def extract_data_from_pdf(pdf_path):
    pdf_path = os.path.abspath(pdf_path)
    pdf_reader = PdfReader(pdf_path)

    pdf_content = "\n".join(page.extract_text(extraction_mode="layout") for page in pdf_reader.pages)

    data_records = []

    for line in pdf_content.splitlines():
        data_fields = [field.strip() for field in re.split(r'\s{4,}', line.strip()) if field.strip()]
        
        if data_fields and data_fields[0][0].isdigit():
            while len(data_fields) < 5:
                data_fields.insert(2, '')
            data_records.append(tuple(data_fields[:5]))

    return data_records
