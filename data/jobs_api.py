import datetime
import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(rules=("-user", "-user"))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<users_id>', methods=['GET'])
def get_one_news(jobs_id):
    if type(jobs_id) != int or jobs_id < 1:
        return jsonify({'error': 'Incorect'})

    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(rules=("-user", "-user"))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'collaborators', 'start_date',
                  'end_date', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    if 'id' in request.json.keys():
        if db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first() is not None:
            return jsonify({'error': 'Id already exists'})
    job = Jobs(
        job=request.json["job"],
        work_size=int(request.json["work_size"]),
        collaborators=request.json["collaborators"],
        start_date=datetime.date(int(request.json["start_date"].split('-')[0]),
                                 int(request.json["start_date"].split('-')[1]),
                                 int(request.json["start_date"].split('-')[2])),
        end_date=datetime.date(int(request.json["start_date"].split('-')[0]),
                               int(request.json["start_date"].split('-')[1]),
                               int(request.json["start_date"].split('-')[2])),
        is_finished=request.json["is_finished"],
        team_leader=int(request.json["team_leader"]),
    )
    if 'id' in request.json.keys():
        job.id = request.json['id']
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:users_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['PUT'])
def edit_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})
    job = db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if not job:
        return jsonify({'error': 'Not found'})

    if 'job' in request.json:
        job.job = request.json['job']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'start_date' in request.json:
        job.start_date = request.json['start_date']
    if 'end_date' in request.json:
        job.end_date = request.json['end_date']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    if 'team_leader' in request.json:
        job.team_leader = request.json['team_leader']

    db_sess.commit()
    return jsonify({'success': 'OK'})
