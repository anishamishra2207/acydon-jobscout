import requests
import sqlite3

url = "https://himalayas.app/jobs/api?limit=20&offset=0"

response = requests.get(url)
data = response.json()

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

for job in data["jobs"]:

    source_id = str(
        job.get("id")
        or job.get("applicationLink")
        or job.get("title")
    )

    cursor.execute("""
        INSERT OR IGNORE INTO jobs
        (source_id, title, company, job_type, salary, description, job_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        source_id,
        job.get("title"),
        job.get("companyName"),
        job.get("employmentType"),
        job.get("salary"),
        job.get("description"),
        job.get("applicationLink")
    ))

conn.commit()
conn.close()

print("Jobs fetched and saved successfully!")