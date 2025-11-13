from models import User, Role, Incident

def test_user_password_hashing(app):
    user = User(username="john", first_name="John", last_name="Doe", middle_name="", role_id=1)
    user.set_password("secret")
    assert user.password_hash != "secret"
    assert user.check_password("secret")
    assert not user.check_password("wrong")

def test_role_repr(app):
    role = Role(name="admin", description="Administrator")
    assert "admin" in repr(role)

def test_incident_repr(app):
    incident = Incident(reg_number="R-001", short_description="Test incident")
    assert "Test incident" in repr(incident)
