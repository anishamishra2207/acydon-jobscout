import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM jobs")

jobs = cursor.fetchall()

for job in jobs:
    print(job)

print("\nTotal jobs:", len(jobs))

conn.close()