import flask
from flask import jsonify
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


@blueprint.route('/api/jobs/<jobs_id>', methods=['GET'])
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
