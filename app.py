import pandas as pd
import plotly.express as px
import streamlit as st

from analytics import applications_over_time, summary_metrics
from database import add_application, delete_application, get_applications, update_status

STATUSES = ["Interested", "Applied", "Interview", "Offer", "Rejected"]

st.set_page_config(page_title="ApplyTrack", page_icon="📋", layout="wide")
st.title("ApplyTrack")
st.caption("A simple internship and job application tracker.")

with st.sidebar:
    st.header("Add application")
    with st.form("add_application"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        status = st.selectbox("Status", STATUSES, index=1)
        date_applied = st.date_input("Date applied")
        location = st.text_input("Location")
        job_url = st.text_input("Job link")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add application", use_container_width=True)

    if submitted:
        if not company.strip() or not role.strip():
            st.error("Company and role are required.")
        else:
            add_application(
                company.strip(),
                role.strip(),
                status,
                date_applied.isoformat(),
                location.strip(),
                job_url.strip(),
                notes.strip(),
            )
            st.success("Application added.")
            st.rerun()

applications = get_applications()
metrics = summary_metrics(applications)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Applications", metrics["total"])
m2.metric("Interviews", metrics["interviews"])
m3.metric("Offers", metrics["offers"])
m4.metric("Response rate", f"{metrics['response_rate']:.0%}")

if applications.empty:
    st.info("Add your first application from the sidebar.")
    st.stop()

st.subheader("Applications")
f1, f2 = st.columns(2)
status_filter = f1.multiselect("Filter by status", STATUSES)
search = f2.text_input("Search company or role")

filtered = applications.copy()
if status_filter:
    filtered = filtered[filtered["status"].isin(status_filter)]
if search.strip():
    query = search.strip().lower()
    filtered = filtered[
        filtered["company"].str.lower().str.contains(query)
        | filtered["role"].str.lower().str.contains(query)
    ]

display = filtered[["id", "company", "role", "status", "date_applied", "location"]].copy()
display["date_applied"] = display["date_applied"].dt.date
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("Update an application")
labels = {
    f"#{row.id} · {row.company} — {row.role}": row.id
    for row in applications.itertuples()
}
selected_label = st.selectbox("Application", list(labels))
selected_id = labels[selected_label]

u1, u2 = st.columns([2, 1])
current_status = applications.loc[applications["id"] == selected_id, "status"].iloc[0]
new_status = u1.selectbox("New status", STATUSES, index=STATUSES.index(current_status))

if u1.button("Update status", use_container_width=True):
    update_status(selected_id, new_status)
    st.success("Status updated.")
    st.rerun()

if u2.button("Delete", type="secondary", use_container_width=True):
    delete_application(selected_id)
    st.success("Application deleted.")
    st.rerun()

st.subheader("Application activity")
timeline = applications_over_time(applications)
if not timeline.empty:
    st.plotly_chart(
        px.bar(timeline, x="date", y="applications", title="Applications submitted over time"),
        use_container_width=True,
    )

st.subheader("Status breakdown")
status_counts = applications["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]
st.plotly_chart(
    px.pie(status_counts, names="status", values="count", hole=0.45),
    use_container_width=True,
)
