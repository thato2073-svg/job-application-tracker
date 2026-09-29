from __future__ import annotations
import pandas as pd

def summary_metrics(frame: pd.DataFrame) -> dict[str, float]:
    if frame.empty:
        return {"total": 0, "interviews": 0, "offers": 0, "response_rate": 0.0}
    statuses = frame["status"]
    interviews = int((statuses == "Interview").sum())
    offers = int((statuses == "Offer").sum())
    responses = int(statuses.isin(["Interview", "Offer", "Rejected"]).sum())
    return {
        "total": len(frame),
        "interviews": interviews,
        "offers": offers,
        "response_rate": responses / len(frame),
    }

def applications_over_time(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["date", "applications"])
    daily = (
        frame.assign(date=pd.to_datetime(frame["date_applied"]).dt.date)
        .groupby("date")
        .size()
        .reset_index(name="applications")
    )
    return daily
