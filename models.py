from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Users {self.username}>'
    
class Responden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    npm = db.Column(db.String(20), unique=True, nullable=False)
    responses = db.Column(db.Text, nullable=False)
    Input = db.Column(db.String(50), nullable=False)
    Processing = db.Column(db.String(50), nullable=False)
    Perception = db.Column(db.String(50), nullable=False)
    Understanding = db.Column(db.String(50), nullable=False)

    def __init__(self, name, npm, responses, Input, Processing, Perception, Understanding):
        self.name = name
        self.npm = npm
        self.responses = responses
        self.Input = Input
        self.Processing = Processing
        self.Perception = Perception
        self.Understanding = Understanding