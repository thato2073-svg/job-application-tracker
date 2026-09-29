from pathlib import Path
import database

def test_crud_and_stats(tmp_path: Path):
    db=tmp_path/"test.db"
    database.add_application("PCL","Software Intern","Applied","2026-09-29",db_path=db)
    database.add_application("Deloitte","Analyst Intern","Interview","2026-09-28",db_path=db)
    rows=database.get_applications(db_path=db)
    assert len(rows)==2
    assert database.stats(db)["interviews"]==1
    app_id=rows[0]["id"]
    row=database.get_application(app_id,db)
    database.update_application(app_id,row["company"],row["role"],"Offer",row["date_applied"],db_path=db)
    assert database.get_application(app_id,db)["status"]=="Offer"
    database.delete_application(app_id,db)
    assert len(database.get_applications(db_path=db))==1

def test_search_and_filter(tmp_path: Path):
    db=tmp_path/"test.db"
    database.add_application("PCL","Software Intern","Applied","2026-09-29",db_path=db)
    database.add_application("Deloitte","Analyst Intern","Interview","2026-09-28",db_path=db)
    assert len(database.get_applications(search="software",db_path=db))==1
    assert len(database.get_applications(status="Interview",db_path=db))==1
