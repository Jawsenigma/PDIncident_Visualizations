import os
import sqlite3

def generate_summary():
    db_file = os.path.join("resources", "normanpd.db")
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT nature, COUNT(*) FROM incident_reports GROUP BY nature ORDER BY nature ASC")
        results = cursor.fetchall()
    
    return '\n'.join(f"{nature}|{count}" for nature, count in results) + '\n'

def remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def remove_database():
    db_file = os.path.join("resources", "normanpd.db")
    try:
        os.remove(db_file)
    except FileNotFoundError:
        print("Database file not found.")
