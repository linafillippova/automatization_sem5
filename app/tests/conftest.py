import pytest
from app import create_app, db
from models import Role, User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "testsecret"
    })

    with app.app_context():
        db.drop_all()   # Очищаем перед каждым тестом
        db.create_all()

        # Проверяем, нет ли роли с таким именем
        if not Role.query.filter_by(name="administrator").first():
            admin_role = Role(name="administrator", description="Admin role")
            db.session.add(admin_role)
            db.session.commit()

        # Создаем пользователя-админа
        admin = User(username="admin", first_name="Test", last_name="Admin", middle_name="",
                     role_id=admin_role.id)
        admin.set_password("password")
        db.session.add(admin)
        db.session.commit()

    yield app

    # После каждого теста удаляем БД
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
