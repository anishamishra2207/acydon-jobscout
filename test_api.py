import requests

url = "https://himalayas.app/jobs/api?limit=5&offset=0"

response = requests.get(url)

data = response.json()

for job in data["jobs"]:
    print("Title:", job.get("title"))
    print("Company:", job.get("companyName"))
    print("Type:", job.get("employmentType"))
    print("Salary:", job.get("salary"))
    print("Description:", job.get("description", "")[:100])
    print("Job URL:", job.get("applicationLink"))
    print("-" * 50)