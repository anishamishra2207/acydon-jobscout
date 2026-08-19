import requests
import sqlite3

URL = "https://himalayas.app/jobs/api?limit=20&offset=0"

try:
    response = requests.get(
        URL,
        timeout=15,
        headers={
            "User-Agent": "JobScout/1.0"
        }
    )

    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    if not jobs:
        print("No jobs returned from the source.")
    else:
        conn = sqlite3.connect("jobs.db")
        cursor = conn.cursor()

        for job in jobs:

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

        print(f"Successfully fetched and stored {len(jobs)} jobs.")

except requests.exceptions.Timeout:
    print("The job source timed out. Please try again later.")

except requests.exceptions.RequestException as e:
    print(f"Could not fetch jobs from the source: {e}")

except ValueError:
    print("The source returned an invalid JSON response.")

except Exception as e:
    print(f"Unexpected error: {e}")