import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT UNIQUE,
    title TEXT,
    company TEXT,
    job_type TEXT,
    salary TEXT,
    description TEXT,
    job_url TEXT
)
""")

conn.commit()
conn.close()

print("Database ready!")