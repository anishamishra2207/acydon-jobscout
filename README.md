# 🔎 JobScout – Smart Job Discovery Platform

### Find opportunities that match your future.

JobScout is a job discovery web application that collects real job
listings from the public Himalayas Jobs API, stores them in SQLite,
and provides a clean Streamlit interface for searching, filtering,
sorting, and opening job opportunities.

## 🚀 Live Demo

👉 https://acydon-jobscout.streamlit.app/

## 💻 GitHub Repository

👉 https://github.com/anishamishra2207/acydon-jobscout

---

## ✨ Features

- 🔎 Search jobs by title, company, or keyword
- 🎯 Filter jobs by job type
- 🏢 Filter jobs by company
- ↕️ Sort job listings
- ✨ Smart Match based on user skills
- ♡ Save jobs during the current session
- 🔗 Open the original job/application page
- 🧹 Clean and readable job descriptions
- 🗄️ SQLite-based local storage
- 🔄 Duplicate-safe job ingestion
- 📊 Displays the number of available and matching jobs
- 🎨 Responsive, professional Streamlit UI

---

## 🏗️ Architecture

```text
                Himalayas Jobs API
                        │
                        ▼
                fetch_jobs.py
                        │
                        ▼
                  JSON Response
                        │
                        ▼
                 Field Extraction
                        │
                        ▼
                    SQLite
                   jobs.db
                        │
                        ▼
                   app.py
                 Streamlit UI
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
         Search      Filters      Sorting
            │           │           │
            └───────────┼───────────┘
                        ▼
                 Job Opportunities
                        │
                        ▼
              Original Application URL
