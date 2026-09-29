# ApplyTrack

A lightweight job and internship application tracker built with **Flask, SQLite, HTML and CSS**.

I built ApplyTrack as a simple alternative to tracking internship applications in a spreadsheet. It focuses on practical CRUD operations, database persistence, filtering and a clean responsive interface.

## Features

- Add job and internship applications
- Track company, role, date, location, link and notes
- Status workflow: Interested, Applied, Interview, Offer, Rejected
- Edit and delete applications
- Search by company or role
- Filter by application status
- Dashboard totals for applications, interviews and offers
- Response-rate calculation
- SQLite persistence
- Responsive custom HTML/CSS interface
- pytest coverage for database operations and filters

## Tech stack

- Python
- Flask
- SQLite
- HTML / CSS
- pytest

## Run locally

```bash
git clone https://github.com/thato2073-svg/job-application-tracker.git
cd job-application-tracker
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## What this project demonstrates

ApplyTrack is intentionally small. The goal is to demonstrate core web-development skills clearly: Flask routing, server-rendered templates, HTML forms, CRUD operations, SQL persistence, filtering, validation and responsive styling.

## Author

**Thato Olayinka**  
Computing Science + Economics, University of Alberta
