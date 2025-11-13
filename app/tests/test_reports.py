from datetime import datetime
from models import Incident, db

def test_report_incident_count(client, app):
    with app.app_context():
        db.session.add(Incident(reg_number="INC002", short_description="Incident A", registration_date=datetime.utcnow()))
        db.session.commit()

    client.post("/login", data={"username": "admin", "password": "password"}, follow_redirects=True)
    response = client.post("/reports/incident_count", data={
        "start_date": "2020-01-01",
        "end_date": "2030-01-01"
    }, follow_redirects=True)

    assert response.status_code == 200
