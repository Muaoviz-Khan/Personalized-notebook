from marshmallow import Schema, fields

class users_schema(Schema):
    id = fields.Int()
    name=fields.Str()
    username = fields.Str()
    email = fields.Str()
    

class notes_schema(Schema):
    nid = fields.Int()
    data = fields.Str()
    date = fields.DateTime()
    userid = fields.Int()