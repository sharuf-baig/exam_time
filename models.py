from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User_details"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)