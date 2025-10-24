import os
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Role, User
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from routes import routes
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '3266a513ac62f8c4be0670900e7fd71342a62f0fc685d900c38985938f49ca39')


# Инициализация SQLAlchemy
db.init_app(app)

# Инициализация Flask-Migrate для миграций базы данных
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'
login_manager.login_message = "Для выполнения данного действия необходимо пройти процедуру аутентификации"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Регистрация blueprint с маршрутами
app.register_blueprint(routes)

from functools import wraps



def create_app():
    with app.app_context():
        db.create_all()
        print("Создание таблиц выполнено")
    return app



if __name__ == '__main__':
    app = create_app()
    #with app.app_context():
     #   print(app.url_map)
    app.run(debug=True)