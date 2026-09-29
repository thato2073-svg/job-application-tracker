# ApplyTrack

A simple internship and job application tracker built with Python, Streamlit, SQLite, Pandas and Plotly.

ApplyTrack helps students keep track of where they applied, what stage each application is in and how their search is progressing.

## Features

- Add company, role, location, date applied, job link and notes
- Track status: Interested, Applied, Interview, Offer or Rejected
- Search by company or role
- Filter by status
- Update application status
- Delete applications
- View total applications, interviews, offers and response rate
- View applications submitted over time
- View status breakdown
- Store everything locally in SQLite

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
streamlit run app.py
```

## Why I built it

I wanted a lightweight way to track internship applications without using a spreadsheet. This project focuses on practical CRUD operations, local persistence and simple analytics.

## Tech stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- pytest

## Author

**Thato Olayinka**  
Computing Science + Economics, University of Alberta
