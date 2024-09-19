from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timezone

class Userstc(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    username = db.Column(db.String(30), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    notes=db.relationship('Notes')

    @property
    def password(self):
        raise AttributeError("Password is not readable")
        
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_pass(self, password):
        return check_password_hash(self._password, password)
    

class Notes(db.Model):
    __tablename__ = "note"
    nid= db.Column(db.Integer,primary_key=True)   
    data=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime(timezone=True),default=datetime.now(timezone.utc)) 
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
        
class TokenBlacklist(db.Model):
    __tablename__ = 'blacklistedtoken'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)