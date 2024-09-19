from flask import jsonify,request,Blueprint
from app import db
from app.notes.model import Userstc

register=Blueprint("register",__name__)

@register.route('/register', methods=['POST'])
def post():
    data = request.get_json()

    if Userstc.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if Userstc.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    if len(data["name"]) < 2:
        return jsonify({'message': 'First name must be greater than 1 character.'}), 400
    
    if len(data["password"]) < 7:
        return jsonify({'message': 'Password must be at least 7 characters.'}), 400
    
    user = Userstc(
        name=data['name'],
        username=data['username'],
        password=data['password'],
        email=data['email']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})