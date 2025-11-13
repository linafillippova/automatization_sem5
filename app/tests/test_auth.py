def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Логин" in html  # проверяем, что форма загружается

def test_successful_login(client, app):
    with app.app_context():
        response = client.post("/login", data={
            "username": "admin",
            "password": "password"
        }, follow_redirects=True)
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Для выполнения данного действия" not in html  # проверяем, что flash-сообщения об ошибке отсутствуют

def test_failed_login(client):
    response = client.post("/login", data={
        "username": "admin",
        "password": "wrong"
    }, follow_redirects=True)
    html = response.data.decode("utf-8")
    assert "Невозможно аутентифицироваться" in html
