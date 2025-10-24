import os
from app import app, db
from models import User, Role
from werkzeug.security import generate_password_hash

def populate_roles():
    with app.app_context():
        if Role.query.count() == 0:
            admin_role = Role(name='administrator', description='Суперпользователь, имеет полный доступ к системе')
            user_role = Role(name='user', description='Может смотреть')

            db.session.add_all([admin_role, user_role])
            db.session.commit()
            print("Роли добавлены в базу данных.")
        else:
            print("Роли уже существуют в базе данных.")

def populate_users():
    with app.app_context():
        if User.query.count() == 0:
            admin_role = Role.query.filter_by(name='administrator').first()
            user_role = Role.query.filter_by(name='user').first()

            if not admin_role or not user_role:
                print("Роли не найдены. Запустите сначала функцию populate_roles.")
                return

            admin_user = User(
                username='admin',
                password_hash=generate_password_hash('admin'),
                first_name='Полина',
                last_name='Филиппова',
                middle_name='Владимировна',
                role=admin_role
            )

            user1 = User(
                username='user',
                password_hash=generate_password_hash('user'),
                first_name='Екатерина',
                last_name='Баранова',
                middle_name='Ивановна',
                role=user_role
            )

            db.session.add_all([admin_user, user1])
            db.session.commit()
            print("Пользователи добавлены в базу данных.")
        else:
            print("Пользователи уже существуют в базе данных.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    populate_roles()
    populate_users()