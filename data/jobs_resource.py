from flask_restful import Resource, reqparse, abort
from flask import jsonify
from . import db_session
from .jobs import Jobs
from .category import Category
import datetime


def abort_if_jobs_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, messsage="Job wasn't found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        dic = {'collaborators': jobs.collaborators, 'end_date': jobs.end_date, 'id': jobs.id,
               'is_finished': jobs.is_finished, 'job': jobs.job, 'start_date': jobs.start_date,
               'team_leader': jobs.team_leader, 'work_size': jobs.work_size, 'categories':
               ', '.join([cat.name for cat in jobs.categories])}
        return jsonify({'jobs': dic})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(job_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('categories')


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [
            {'collaborators': item.collaborators, 'end_date': item.end_date, 'id': item.id,
             'is_finished': item.is_finished, 'job': item.job, 'start_date': item.start_date,
             'team_leader': item.team_leader, 'work_size': item.work_size, 'categories':
                 ', '.join([cat.name for cat in item.categories])}
            for item in jobs
        ]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            team_leader=args['team_leader'],
            start_date=datetime.date(int(args["start_date"].split('-')[0]),
                                     int(args["start_date"].split('-')[1]),
                                     int(args["start_date"].split('-')[2])),
            end_date=datetime.date(int(args["end_date"].split('-')[0]),
                                     int(args["end_date"].split('-')[1]),
                                     int(args["end_date"].split('-')[2]))
        )
        if args['categories'] is not None:
            categories = args['categories'].split(', ')
            for cat in categories:
                cat_f = session.query(Category).filter(Category.name == cat).first()
                if not cat_f:
                    cat_n = Category(name=cat)
                    session.add(cat_n)
                    session.commit()
                    cat = cat_n
                else:
                    cat = cat_f

                jobs.categories.append(cat)

        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})
