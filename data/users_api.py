import datetime
import flask
from flask import jsonify, request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(rules=("-user", "-user"))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<users_id>', methods=['GET'])
def get_one_user(users_id):
    users_id = int(users_id)
    if type(users_id) != int or users_id < 1:
        return jsonify({'error': users_id})

    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(rules=("-user", "-user"))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    if 'id' in request.json.keys():
        if db_sess.query(User).filter(User.id == request.json['id']).first() is not None:
            return jsonify({'error': 'Id already exists'})
    user = User(
        surname=request.json["surname"],
        name=request.json["name"],
        age=request.json["age"],
        position=request.json["position"],
        modified_date=datetime.datetime.now(),
        speciality=request.json["speciality"],
        address=request.json["address"],
        email=request.json["email"]
    )
    if 'id' in request.json.keys():
        user.id = request.json['id']
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_user(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['PUT'])
def edit_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' not in request.json:
        return jsonify({'error': 'Bad request'})
    user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if not user:
        return jsonify({'error': 'Not found'})

    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        user.age = request.json['age']
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        user.team_leader = request.json['email']
    user.modified_date = datetime.datetime.now()

    db_sess.commit()
    return jsonify({'success': 'OK'})
