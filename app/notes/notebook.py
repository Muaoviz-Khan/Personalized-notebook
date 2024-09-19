from flask import Blueprint,jsonify,request
from app.auth.deco.auth_req import token_required
from marshmallow import ValidationError
from app.notes.model import Notes
from app.notes.serde import notes_schema
from app import db

notess=Blueprint("notess",__name__)

@notess.route("/view",methods=['GET'])
@token_required
def get(current_user):
    try:
        if Notes.query.filter_by(user_id=current_user.id):
            records=Notes.query.filter_by(user_id=current_user.id)
            valid = notes_schema().dump(records, many=True)
        else:
            return jsonify({'message':'No records found'}), 404
    except ValidationError as error:
        return jsonify({'message':'ValidationError', 'Error':error}), 400
    return jsonify(valid), 200


@notess.route('/add',methods=['POST'])
@token_required
def post(current_user):
    if not (note := request.get_json()):
        return jsonify({'message': 'no data '}), 204
    print(note)
    try:
        va = notes_schema().load(note)
    except ValidationError as e:
        return jsonify({'message': 'Validation Error', 'errors': e.messages}), 422
    add_note = Notes(data=note['data'], user_id=current_user.id)
    db.session.add(add_note)
    db.session.commit()
    return jsonify({'message': 'notes added'}), 200

@notess.route('/update',methods=['PUT'])
@token_required
def put(current_user):
    if not (data:=request.get_json()):
        return jsonify({'message':'no data provided'}), 204
    try:
        va = notes_schema().load(data)
    except ValidationError as e:
        return jsonify({'message':'Validation Error', 'errors': e}), 422
    except Exception as e:
        return jsonify({'error':e})
    
    Notes.query.filter_by(nid=data['nid']).update(data,synchronize_session=False)
    db.session.commit()
    return jsonify({'message':'note Updated successfully'})

@notess.route('/delete',methods=['DELETE'])
@token_required
def delete(current_user): 
    if not (data := request.get_json()):
        return jsonify({'message':"no data provided"}), 204
       
    Notes.query.filter_by(nid=data['nid']).delete()
    db.session.commit()
    return jsonify({'message': f"{data['nid']} was successfully deleted"}), 200