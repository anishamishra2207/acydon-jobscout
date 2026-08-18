# 🔎 JobScout – Smart Job Discovery Platform

JobScout is a simple job discovery web application built using **Python and Streamlit**.

The application collects job opportunities from a public jobs API, stores the job data in a **SQLite database**, and displays the available jobs through a clean and user-friendly interface.

## 🚀 Features

- Fetches job data from a public API
- Stores job information in SQLite
- Displays job title, company, job type, salary, and description
- Search jobs by title or company
- Provides direct links to job opportunities
- Simple and responsive Streamlit interface

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application interface
- **REST API** – Job data collection
- **SQLite** – Local job database
- **Requests** – API communication

## 🔄 How It Works

```text
Public Jobs API
      ↓
Python API Fetcher
      ↓
SQLite Database
      ↓
Streamlit Application
      ↓
User searches and explores jobs
