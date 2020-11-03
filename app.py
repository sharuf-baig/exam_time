#importing all the required libraries
from flask import Flask, session,request,render_template,redirect,flash,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import requests
import time
from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
from docx import Document
from wtforms.validators import ValidationError
from coolname import generate_slug
from datetime import timedelta, datetime
#####################################
app = Flask(__name__)
app.secret_key= 'temtemp'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)
#vefify for login
def is_logged(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'user' in session is not None:
			return f(*args, **kwargs)
		else:
			flash('Please login','danger')
			return redirect('/')
	return wrap
def doctodict(filepath):
	document = Document(filepath)
	data={}
	count=1
	for table in document.tables:
		temp = {}
		for rowNo,_ in enumerate(table.rows):
			temp[table.cell(rowNo, 0).text]=table.cell(rowNo, 1).text
		data[count] = temp
		count+=1
 
	return data
class UploadForm(FlaskForm):
	subject = StringField('Subject')
	topic = StringField('Topic')
	doc = FileField('Docx Upload', validators=[FileRequired()])
	start_date = DateField('Start Date')
	start_time = TimeField('Start Time', default=datetime.utcnow()+timedelta(hours=5.5))
	end_date = DateField('End Date')
	end_time = TimeField('End Time', default=datetime.utcnow()+timedelta(hours=5.5))
	show_result = BooleanField('Show Result after completion')
	neg_mark = BooleanField('Enable negative marking')
	duration = IntegerField('Duration(in min)')
	password = StringField('Test Password', [validators.Length(min=3, max=6)])

	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("End date must not be earlier than start date.")
	
	def validate_end_time(form, field):
		start_date_time = datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		end_date_time = datetime.strptime(str(form.end_date.data) + " " + str(field.data),"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
		if start_date_time >= end_date_time:
			raise ValidationError("End date time must not be earlier/equal than start date time")
	
	def validate_start_date(form, field):
		if datetime.strptime(str(form.start_date.data) + " " + str(form.start_time.data),"%Y-%m-%d %H:%M:%S") < datetime.now():
			raise ValidationError("Start date and time must not be earlier than current")

#various routes for the website
#login part
@app.route("/",methods=["GET","POST"])
def login():
	if session.get("user") is None:
		if request.method == "GET":
			return render_template('index.html',info=['login','UserName','Password','register'])
		else:
			name = request.form.get("name")
			password =request.form.get("password")
			user = User.query.filter_by(name=name).first()
			if user is None:
				flash('No user found with that sort of name')
				return redirect("/")
			elif not check_password_hash(user.password,password):
				flash("you password is incorrect")
				return redirect("/")
			else:
				session["user"]=user.name
				return redirect('/home')
	else:
		return redirect('/home')
@app.route("/register",methods=["GET","POST"])		
def register():
	if session.get("user") is None:
		if request.method == "GET":
			return render_template('index.html',info=['register','Your UserName','Your Password','login'])
		elif request.method == "POST":
			name = request.form.get("name")
			password =request.form.get("password")
			email =request.form.get("email")
			password_hash = generate_password_hash(password)
			user = User.query.filter_by(name=name).first() or User.query.filter_by(email=email).first()
			if user is None: 
				user = User(name=name,password=password_hash,email=email)
				session["user"]=user.name	
				db.session.add(user)
				db.session.commit()
				return redirect('/home')
			else:
				flash('User Name/Email is Taken')
				return redirect('/register')	
	else:
		return redirect('/home')
@app.route("/home",methods=["GET","POST"])
@is_logged
def home():
	return render_template('dashboard.html',info=['Give Test','Results','Student Results','Create Test'])            
@app.route("/logout")
@is_logged
def logout():
	session.clear()
	return redirect("/")
@app.route('/create-test', methods = ['GET', 'POST'])
@is_logged
def create_test():
	form = UploadForm()
	if request.method == 'POST' and form.validate_on_submit():
		f = form.doc.data
		filename = secure_filename(f.filename)
		f.save('questions/' + filename)
		d = doctodict('questions/' + f.filename.replace(' ', '_').replace('(','').replace(')',''))
		test_id = generate_slug(2)
		try:
			for no, data in d.items():
				marks = data['((MARKS)) (1/2/3...)']
				a = data['((OPTION_A))']
				b = data['((OPTION_B))']
				c = data['((OPTION_C))']
				d = data['((OPTION_D))']
				question = data['((QUESTION))']
				correct_ans = data['((CORRECT_CHOICE)) (A/B/C/D)']
				explanation = data['((EXPLANATION)) (OPTIONAL)']

				tquestion = T_question(test_id=test_id,question_id=no,question=question,a=a,b=b,c=c,d=d,c_ans=correct_ans,marks=marks,explanation=explanation)
				db.session.add(tquestion)
				db.session.commit()
			start_date = form.start_date.data
			end_date = form.end_date.data
			start_time = form.start_time.data
			end_time = form.end_time.data
			start_date_time = str(start_date) + " " + str(start_time)
			end_date_time = str(end_date) + " " + str(end_time)
			show_result = form.show_result.data
			neg_mark = form.neg_mark.data

			duration = int(form.duration.data)*60
			password = form.password.data
			subject = form.subject.data
			topic = form.topic.data
			test=Test(test_id=test_id,start=start_date_time,end=end_date_time,duration=duration,show_result=show_result,password=password,subject=subject,topic=topic,neg=neg_mark)
			db.session.add(test)
			db.session.commit()
			flash(f'Test ID: {test_id}', 'success')
			return redirect(url_for('home'))
		except Exception as e:
			print(e)
			flash('Invalid Input File Format','danger')
			return redirect(url_for('create_test'))
		
	return render_template('create_test.html' , form = form)
@app.route('/give-test', methods = ['GET', 'POST'])
@is_logged
def give_test():

	tests = Test.query.all()
	
	
	return render_template('show_tests.html',tests=tests)	
