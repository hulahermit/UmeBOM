from . import user_bp
from .. import db
from sqlalchemy import event
from flask import jsonify, request
from werkzeug.security import generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email
        }

def get_password(word):
    return generate_password_hash(word, method='pbkdf2:sha256')

@event.listens_for(User.__table__, 'after_create')
def insert_initial_items(*args, **kwargs):
    db.session.add(User(username='admin', password=get_password('admin')))

@user_bp.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        name=data['name'],
        email=data['email'],
        password=get_password(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id}), 201

@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data['username']
    user.first_name = data['name']
    user.last_name = data['email']
    if data.get('password'):
        user.password = get_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
