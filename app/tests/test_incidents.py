from models import Incident

def test_add_incident(client, app):
    # Авторизация перед добавлением
    client.post("/login", data={"username": "admin", "password": "password"}, follow_redirects=True)

    response = client.post("/incidents/add", data={
        "reg_number": "INC001",
        "short_description": "Тестовое происшествие"
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        incident = Incident.query.filter_by(reg_number="INC001").first()
        assert incident is not None
        assert incident.short_description == "Тестовое происшествие"


def test_list_incidents_requires_login(client):
    response = client.get("/incidents", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Для выполнения данного действия необходимо пройти процедуру аутентификации" in html
