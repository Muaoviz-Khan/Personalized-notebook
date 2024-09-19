from flask import jsonify,request,Blueprint,current_app
import jwt
from app.notes.model import Userstc
from datetime import datetime, timedelta,timezone

login=Blueprint("login",__name__)


@login.route('/login', methods=['POST'])
def post():
    credentials = request.get_json()
    user = Userstc.query.filter_by(username=credentials["username"]).first()
    
    if not user or not user.verify_pass(credentials["password"]):
        return jsonify({'message': 'Invalid username or password'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=10)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    response = jsonify({'token': token})
    response.set_cookie("token", token, httponly=True) 
    return response