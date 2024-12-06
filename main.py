import argparse 
from project3.fetch import fetch_pdf
from project3.extract import extract_data_from_pdf
from project3.createdb import create_new_db, populate_new_db
from project3.status import generate_summary, remove_file

def generate_report_from_pdf(url):
    try:
        pdf_file_path = fetch_pdf(url)
        if pdf_file_path is None:
            return

        records = extract_data_from_pdf(pdf_file_path)
        if not records:
            print("Data extraction from PDF failed. Exiting.")
            return

        create_new_db()
        populate_new_db(records)
        summary_report = generate_summary()
        print(summary_report)
        remove_file(pdf_file_path)

    except Exception as e:
        print(f"An unexpected error occurred: {e}. Exiting.")
        return

def main():
    argument_parser = argparse.ArgumentParser(description='Generate a report from a given PDF URL.')
    argument_parser.add_argument('--incidents', type=str, required=True, help='PDF URL containing incidents data')

    args = argument_parser.parse_args()
    
    pdf_url = args.incidents
    generate_report_from_pdf(pdf_url)

if __name__ == '__main__':
    main()
