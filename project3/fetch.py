import os
import re
import requests

def fetch_pdf(pdf_url):
    response = requests.get(pdf_url)
    if response.ok:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', pdf_url)
        date_identifier = match.group(1) if match else os.path.splitext(os.path.basename(pdf_url))[0]
        
        temp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporary')
        os.makedirs(temp_folder, exist_ok=True)
        file_path = os.path.join(temp_folder, f"{date_identifier}.pdf")

        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path

    print(f"Failed to fetch PDF. HTTP Status code: {response.status_code}")
    return None
