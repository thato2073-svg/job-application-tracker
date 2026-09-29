from pathlib import Path
from analytics import summary_metrics
from database import add_application, delete_application, get_applications, update_status

def test_database_crud_and_metrics(tmp_path: Path):
    db = tmp_path / "test.db"
    add_application("OpenAI", "Software Intern", "Applied", "2026-09-29", db_path=db)
    add_application("Example Co", "Data Intern", "Interview", "2026-09-28", db_path=db)

    frame = get_applications(db)
    assert len(frame) == 2

    metrics = summary_metrics(frame)
    assert metrics["total"] == 2
    assert metrics["interviews"] == 1
    assert metrics["response_rate"] == 0.5

    app_id = int(frame.iloc[0]["id"])
    update_status(app_id, "Offer", db)
    updated = get_applications(db)
    assert "Offer" in updated["status"].tolist()

    delete_application(app_id, db)
    assert len(get_applications(db)) == 1
