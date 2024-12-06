import os
import sqlite3

def create_new_db():
    resource_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources")
    os.makedirs(resource_folder, exist_ok=True)
    db_file_path = os.path.abspath(os.path.join("resources", "normanpd.db"))
    
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

    with sqlite3.connect(db_file_path) as connection:
        connection.execute(""" 
            CREATE TABLE incident_reports (
                time TEXT,
                number TEXT,
                location TEXT,
                nature TEXT,
                ori TEXT
            )
        """)

def populate_new_db(data):
    db_file_path = os.path.abspath(os.path.join("resources", "normanpd.db"))

    with sqlite3.connect(db_file_path) as connection:
        connection.executemany("INSERT INTO incident_reports VALUES (?, ?, ?, ?, ?)", data)
