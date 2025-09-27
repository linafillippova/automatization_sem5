# app/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    patronymic = db.Column(db.String(100))
    address = db.Column(db.String(255))
    convictions_count = db.Column(db.Integer, default=0)

    # Связь с IncidentPerson
    incident_roles = db.relationship('IncidentPerson', backref='person', lazy='dynamic')

    def __repr__(self):
        return f'<Person {self.last_name} {self.first_name} {self.patronymic}>'

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String(50), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    short_description = db.Column(db.String(255), nullable=False) # Краткая фабула (тип происшествия)

    # Информация о принятом решении
    decision_status = db.Column(db.String(50)) # Например: "Отказано в возбуждении", "Уголовное дело возбуждено", "Отправлено по территориальному признаку"
    case_reg_number = db.Column(db.String(50)) # Регистрационный номер заведенного уголовного дела

    # Связь с IncidentPerson
    incident_participants = db.relationship('IncidentPerson', backref='incident', lazy='dynamic')

    def __repr__(self):
        return f'<Incident {self.reg_number} - {self.short_description}>'

class IncidentPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Например: "Виновник", "Потерпевший", "Подозреваемый", "Свидетель"

    def __repr__(self):
        return f'<IncidentPerson Incident: {self.incident_id}, Person: {self.person_id}, Role: {self.role}>'
