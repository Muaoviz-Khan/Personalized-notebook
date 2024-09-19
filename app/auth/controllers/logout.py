from flask import jsonify,request,make_response,Blueprint
from app import db
from datetime import datetime,timezone
from app.auth.deco.auth_req import token_required
from app.notes.model import TokenBlacklist


logout=Blueprint("logout",__name__)

@logout.route("/logout", methods=['POST'])
@token_required
def post(current_user):
    token = request.cookies.get("currentuser")
    if token:
        blacklist_token = TokenBlacklist(token=token, blacklisted_on=datetime.now(timezone.utc))
        db.session.add(blacklist_token)
        db.session.commit()
    response = make_response(jsonify({'message': 'Logout successfull'}))
    response.delete_cookie('currentuser')
    return response
