from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user_details"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)

class T_question(db.Model):
    __tablename__ = "tquestions"
    test_id = db.Column(db.String,primary_key=True)
    question_id=db.Column(db.String,primary_key=True)
    question = db.Column(db.Text,nullable=False)
    a = db.Column(db.String,nullable=False)
    b = db.Column(db.String,nullable=False)
    c = db.Column(db.String,nullable=False)
    d = db.Column(db.String,nullable=False)
    c_ans = db.Column(db.String,nullable=False)
    marks = db.Column(db.Integer)
    explanation = db.Column(db.Text,nullable=True)

class Test(db.Model):
    __tabelname__='test'
    test_id=db.Column(db.String,primary_key=True)
    start=db.Column(db.String,nullable=False)
    end=db.Column(db.String,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    show_result=db.Column(db.Boolean,default=False)
    password=db.Column(db.String,default='test')
    subject=db.Column(db.String,nullable=False)
    topic=db.Column(db.String)
    neg=db.Column(db.Boolean,default=False)
    name = db.Column(db.String,nullable=False)

class StudentTI(db.Model):
    __tablename__ ='s_testinfo'
    name = db.Column(db.String,nullable=False,primary_key=True)
    test_id  = db.Column(db.String,nullable=False,primary_key=True)
    time_left = db.Column(db.Integer,nullable=False)
    completed = db.Column(db.Boolean,default=False)

class Student(db.Model):
    __tablename__='students'
    name = db.Column(db.String,nullable=False,primary_key=True)
    test_id  = db.Column(db.String,nullable=False,primary_key=True)
    question_id  = db.Column(db.String,nullable=False,primary_key=True) 
    ans = db.Column(db.String,nullable=False)