import os
import datetime
from data import db_session, api
from werkzeug.exceptions import abort
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from flask import Flask, request
from flask import render_template, redirect
from forms.user import RegisterForm
from forms.LoginForm import LoginForm
from forms.job import JobsForm
from forms.department import DepartmentForm
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    f = False
    a = False
    if f:
        try:
            os.remove('db/mars_explorer.db')
        except FileNotFoundError:
            pass

    db_session.global_init("db/mars_explorer.db")
    if a:
        user0 = User()
        user0.surname = 'Scott'
        user0.name = 'Ridley'
        user0.age = 21
        user0.position = 'captain'
        user0.speciality = 'research engineer'
        user0.address = 'module_1'
        user0.email = 'scott_chief@mars.org'
        db_sess = db_session.create_session()
        db_sess.add(user0)
        db_sess.commit()

        user1 = User()
        user1.surname = 'BigCat'
        user1.name = 'Floppa'
        user1.age = 15
        user1.position = 'Russian Cat'
        user1.speciality = 'war criminal'
        user1.address = 'module_1'
        user1.email = 'floppa@mars.org'
        db_sess = db_session.create_session()
        db_sess.add(user1)
        db_sess.commit()

        user2 = User()
        user2.surname = 'Zhabkins'
        user2.name = 'Zhaba'
        user2.age = 1
        user2.position = 'slave'
        user2.speciality = 'programmer'
        user2.address = 'boloto'
        user2.email = 'CyberZhaba@mars.frog'
        db_sess = db_session.create_session()
        db_sess.add(user2)
        db_sess.commit()

        user3 = User()
        user3.surname = 'Darkholme'
        user3.name = 'Van'
        user3.age = 31
        user3.position = 'boss of the gym'
        user3.speciality = 'dungeon master'
        user3.address = 'gym'
        user3.email = 'van@gachi.org'
        db_sess = db_session.create_session()
        db_sess.add(user3)
        db_sess.commit()

        job0 = Jobs(team_leader=1, job='deployment of residential modules 1 and 2', work_size=15,
                    collaborators='2, 3', start_date=datetime.date(2022, 1, 23), is_finished=False,
                    end_date=datetime.date(2022, 1, 24))
        db_sess = db_session.create_session()
        db_sess.add(job0)
        db_sess.commit()

        job1 = Jobs(team_leader=4, job='building gym', work_size=10,
                    collaborators='4', start_date=datetime.date(2022, 2, 27), is_finished=True,
                    end_date=datetime.datetime.now())
        db_sess = db_session.create_session()
        db_sess.add(job1)
        db_sess.commit()

        dep = Department(title='A', chief=1, members='1, 2, 3', email='a@a.com')
        db_sess = db_session.create_session()
        db_sess.add(dep)
        db_sess.commit()
        dep = Department(title='B', chief=1, members='1, 2, 3', email='b@b.com')
        db_sess = db_session.create_session()
        db_sess.add(dep)
        db_sess.commit()

    app.register_blueprint(api.blueprint)
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    param = {"jobs": []}
    for el in db_sess.query(Jobs).all():
        job = {"id": el.id, "job": el.job, "team_leader": db_sess.query(User).filter(
            User.id == el.team_leader).first().surname + ' ' + db_sess.query(User).filter(
            User.id == el.team_leader).first().name, "collaborators": el.collaborators,
               "finished": el.is_finished, "duration": el.end_date - el.start_date,
               "t_l_id": el.team_leader}

        param["jobs"].append(job)

    return render_template("action.html", **param)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data, name=form.name.data, position=form.position.data,
            age=form.age.data, speciality=form.speciality.data, address=form.address.data,
            email=form.email.data, modified_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        job.team_leader = current_user.id

        db_sess.add(job)
        db_sess.commit()

        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if api.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                              current_user.id == Jobs.team_leader
                                              ).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == id,
                                             current_user.id == Jobs.team_leader
                                             ).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_job.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()

    if current_user.id == 1:
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         current_user.id == Jobs.team_leader
                                         ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def departments_show():
    db_sess = db_session.create_session()
    param = {"departments": []}
    for el in db_sess.query(Department).all():
        department = {"id": el.id, "title": el.title, "chief": db_sess.query(User).filter(
            User.id == el.chief).first().surname + ' ' + db_sess.query(User).filter(
            User.id == el.chief).first().name, "members": el.members,
                      "email": el.email, "t_l_id": el.chief}

        param["departments"].append(department)

    return render_template("departments_show.html", **param)


@app.route('/department_add', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        department.chief = current_user.id

        db_sess.add(department)
        db_sess.commit()

        return redirect('/departments')
    return render_template('add_department.html', title='Добавление департамента',
                           form=form)


@app.route('/department_add/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentForm()
    if api.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Department).filter(Department.id == id).first()
        else:
            dep = db_sess.query(Department).filter(Department.id == id,
                                                   current_user.id == Department.chief
                                                   ).first()
        if dep:
            form.title.data = dep.title
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Department).filter(Department.id == id).first()
        else:
            dep = db_sess.query(Department).filter(Department.id == id,
                                                   current_user.id == Department.chief
                                                   ).first()
        if dep:
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data

            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()

    if current_user.id == 1:
        job = db_sess.query(Department).filter(Department.id == id).first()
    else:
        job = db_sess.query(Department).filter(Department.id == id,
                                               current_user.id == Department.chief
                                               ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


if __name__ == '__main__':
    main()
