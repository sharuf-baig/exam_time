#importing all the required libraries
from flask import Flask, session,request,render_template,redirect,flash,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import time
#####################################
app = Flask(__name__)

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
def home():
	flash('home page')
	return ""            
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")
