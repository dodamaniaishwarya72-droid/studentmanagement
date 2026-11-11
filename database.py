
import sqlite3

def create_database():
    connection = sqlite3.connect("students.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()

create_database()

print("Database created successfully!")
