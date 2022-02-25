import os
import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    os.remove('db/mars_explorer.db')
    db_session.global_init("db/mars_explorer.db")

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
                collaborators='2, 3', start_date=datetime.date(2022, 1, 23), is_finished=False)
    db_sess = db_session.create_session()
    db_sess.add(job0)
    db_sess.commit()

    job1 = Jobs(team_leader=4, job='building gym', work_size=10,
                collaborators='4', start_date=datetime.date(2021, 1, 23), is_finished=True,
                end_date=datetime.datetime.now())
    db_sess = db_session.create_session()
    db_sess.add(job1)
    db_sess.commit()

    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    param = {"jobs": [{"id": 1, "job": 'bebra', "team_leader": 'zhaba', "duration": '15 hours',
                       "collaborators": '1, 4', "finished": True},
                      {"id": 2, "job": 'bebra', "team_leader": 'zhaba', "duration": '15 hours',
                       "collaborators": '1, 4', "finished": False}]}
    param = {"jobs": []}
    for el in db_sess.query(Jobs).all():
        job = {"id": el.id, "job": el.job,
               "team_leader": db_sess.query(User).filter(
                   User.id == el.team_leader).first().surname + ' ' + db_sess.query(User).filter(
                   User.id == el.team_leader).first().name,
               "collaborators": el.collaborators, "finished": el.is_finished}
        if el.is_finished:
            job["duration"] = el.end_date - el.start_date
        else:
            job["duration"] = datetime.datetime.now() - el.start_date

        param["jobs"].append(job)

    return render_template("action.html", **param)


if __name__ == '__main__':
    main()
