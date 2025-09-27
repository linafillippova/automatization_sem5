# app/routes.py
from flask import render_template, request, redirect, url_for, flash, request, Blueprint
from models import db
from models import Incident, Person, IncidentPerson, User
from datetime import datetime
from forms import LoginForm
from flask import session
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required

routes = Blueprint('routes', __name__)

def check_role(role_names):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Требуется аутентификация", "danger")
                return redirect(url_for('routes.login'))

            _role_names = role_names
            if isinstance(_role_names, str):
                _role_names = [_role_names]

            if current_user.role.name not in _role_names:
                flash("У вас недостаточно прав для выполнения данного действия", "danger")
                return redirect(url_for('routes.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


@routes.route('/')
def index():
    return render_template('index.html')

# --- Маршруты для происшествий ---

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('routes.index'))
        else:
            flash('Невозможно аутентифицироваться с указанными логином и паролем', 'danger')
    return render_template('login.html', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes.route('/incidents')
@login_required
def list_incidents():
    incidents = Incident.query.all()
    return render_template('incidents/list_incidents.html', incidents=incidents)

@routes.route('/incidents/add', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def add_incident():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        short_description = request.form['short_description']
        decision_status = request.form.get('decision_status') # Используем .get() для необязательных полей
        case_reg_number = request.form.get('case_reg_number')

        incident = Incident(
            reg_number=reg_number,
            short_description=short_description,
            decision_status=decision_status,
            case_reg_number=case_reg_number,
            registration_date=datetime.utcnow() # Или можно получать из формы
        )
        db.session.add(incident)
        db.session.commit()
        return redirect(url_for('routes.list_incidents'))
    return render_template('incidents/add_incident.html')

@routes.route('/incidents/edit/<int:incident_id>', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def edit_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if request.method == 'POST':
        incident.reg_number = request.form['reg_number']
        incident.short_description = request.form['short_description']
        incident.decision_status = request.form.get('decision_status')
        incident.case_reg_number = request.form.get('case_reg_number')
        db.session.commit()
        return redirect(url_for('routes.list_incidents'))
    return render_template('incidents/edit_incident.html', incident=incident)

# --- Маршруты для лиц ---
@login_required
@routes.route('/persons')
def list_persons():
    persons = Person.query.all()
    return render_template('persons/list_persons.html', persons=persons)


@routes.route('/persons/add', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def add_person():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        patronymic = request.form.get('patronymic')
        address = request.form.get('address')
        convictions_count = int(request.form.get('convictions_count', 0))

        person = Person(
            reg_number=reg_number,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            address=address,
            convictions_count=convictions_count
        )
        db.session.add(person)
        db.session.commit()
        return redirect(url_for('routes.list_persons'))
    return render_template('persons/add_person.html')

@routes.route('/persons/edit/<int:person_id>', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def edit_person(person_id):
    person = Person.query.get_or_404(person_id)
    if request.method == 'POST':
        person.reg_number = request.form['reg_number']
        person.first_name = request.form['first_name']
        person.last_name = request.form['last_name']
        person.patronymic = request.form.get('patronymic')
        person.address = request.form.get('address')
        person.convictions_count = int(request.form.get('convictions_count', 0))
        db.session.commit()
        return redirect(url_for('routes.list_persons'))
    return render_template('persons/edit_person.html', person=person)

# --- Маршруты для отчетов ---

@routes.route('/reports/incident_count', methods=['GET', 'POST'])
@login_required
def report_incident_count():
    incident_count = None
    if request.method == 'POST':
        start_date_str = request.form['start_date']
        end_date_str = request.form['end_date']

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # Важно: Включаем конец дня для корректного подсчета
            end_date = end_date.replace(hour=23, minute=59, second=59)

            incident_count = Incident.query.filter(
                Incident.registration_date >= start_date,
                Incident.registration_date <= end_date
            ).count()
        except ValueError:
            # Обработка ошибки, если формат даты некорректен
            pass # Можно добавить сообщение об ошибке пользователю

    return render_template('reports/incident_count.html', incident_count=incident_count)

@routes.route('/reports/person_incident_count', methods=['GET', 'POST'])
@login_required
def report_person_incident_count():
    person_incident_count = None
    person = None
    if request.method == 'POST':
        person_reg_number = request.form['person_reg_number']
        person = Person.query.filter_by(reg_number=person_reg_number).first()

        if person:
            person_incident_count = IncidentPerson.query.filter_by(person_id=person.id).count()

    return render_template('reports/person_incident_count.html', person_incident_count=person_incident_count, person=person)

# --- Добавление и изменение связей между происшествиями и лицами ---
# Это более сложная часть, потребует отдельного интерфейса для выбора происшествия, лица и роли.
# Для начала, давайте добавим базовые CRUD для IncidentPerson.

@routes.route('/incident_person/add', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def add_incident_person_role():
    if request.method == 'POST':
        incident_id = int(request.form['incident_id'])
        person_id = int(request.form['person_id'])
        role = request.form['role']

        # Проверка, существует ли такое происшествие и лицо
        incident = Incident.query.get(incident_id)
        person = Person.query.get(person_id)

        if incident and person:
            incident_person = IncidentPerson(
                incident_id=incident_id,
                person_id=person_id,
                role=role
            )
            db.session.add(incident_person)
            db.session.commit()
            return redirect(url_for('routes.list_incidents')) # Или на страницу деталей происшествия
        else:
            # Обработка ошибки: инцидент или лицо не найдены
            pass
    # Для формы добавления нам нужно получить списки всех происшествий и лиц
    incidents = Incident.query.all()
    persons = Person.query.all()
    return render_template('incidents/add_incident_person_role.html', incidents=incidents, persons=persons)

@routes.route('/incident/<int:incident_id>/edit_participants', methods=['GET', 'POST'])
@login_required
@check_role('administrator')
def edit_incident_participants(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if request.method == 'POST':
        # Логика обновления участников, может быть сложной.
        # Пример: удалить все старые записи и добавить новые.
        # Более сложный вариант - обновление существующих.
        IncidentPerson.query.filter_by(incident_id=incident_id).delete()
        db.session.commit()

        participants_data = request.form.getlist('participants') # Предполагаем, что данные приходят как список строк 'person_id:role'
        for participant_data in participants_data:
            try:
                person_id_str, role = participant_data.split(':')
                person_id = int(person_id_str)
                person = Person.query.get(person_id)
                if person:
                    incident_person = IncidentPerson(
                        incident_id=incident_id,
                        person_id=person_id,
                        role=role
                    )
                    db.session.add(incident_person)
            except ValueError:
                # Игнорируем некорректные данные
                pass
        db.session.commit()
        return redirect(url_for('routes.list_incidents'))

    # Получаем текущих участников и их роли
    current_participants = IncidentPerson.query.filter_by(incident_id=incident_id).all()
    current_participant_roles = {ip.person_id: ip.role for ip in current_participants}

    # Получаем всех лиц для выбора
    all_persons = Person.query.all()

    return render_template('incidents/edit_incident_participants.html',
                           incident=incident,
                           all_persons=all_persons,
                           current_participant_roles=current_participant_roles)
