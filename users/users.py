from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import mysql.connector
import re

users = Blueprint('users', __name__, template_folder='templates', static_folder='static', static_url_path='/static/users')

mydb = mysql.connector.connect(
	host="localhost", user="root", passwd="root", database="data_scrapper")
cursor = mydb.cursor()

@users.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST"	and 'username' in request.form and 'pass' in request.form:

		username = request.form['username']
		password = request.form['pass']
		if not re.match(r'[^@]+@[^@]+\.[^@]+', username):
			flash(u'Invalid email address', 'alert alert-danger')
		else:
			sql = "SELECT * FROM users WHERE username=%s AND password=%s"
			values = (username, password)
			cursor.execute(sql, values)
			user = cursor.fetchone()

			if user:
				session['loggedin'] = True
				session['id'] = user[0]
				session['username'] = username[0]
				flash('Loggedin successfully')
				return redirect(url_for('users.profile'))
			else:
				flash(u'Username / password incorrect', 'alert alert-danger')
	if 'loggedin' in session:
		return redirect(url_for('users.profile'))
	else:
		title = "ToroMovies | Login"
		return render_template('login.html', title=title)


@users.route('/register', methods=['POST', 'GET'])
def register():
	if 'loggedin' in session:
		return redirect(url_for('users.profile'))
	else:
		if request.method == "POST":
			username = request.form['username']
			password1 = request.form['pass']
			password2 = request.form['pass2']
			if password1 != password2:
				flash('The passwords do not match')
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
				flash('Invalid Email address')
			elif not username or not password1 or not password2:
				flash('Please fill out the form')
			else:
				sql1 = f"SELECT * FROM users WHERE username = '{username}'"
				values1 = (username)
				cursor.execute(sql1)
				account = cursor.fetchone()

				if account:
					flash('The email entered already exists in the database')
				else:
					sql = "INSERT INTO users (username, password) VALUES(%s, %s)"
					values = (username, password1)
					cursor.execute(sql, values)
					mydb.commit()
					flash(u'Registration completed', 'alert alert-success')
					return redirect(url_for('users.login'))
		title = "ToroMovies | Register"
		return render_template('register.html', title=title)

@users.route('/profile')
def profile():
	if 'loggedin' in session:
		sql = f"SELECT * FROM users WHERE user_id={session['id']}"
		cursor.execute(sql)
		user = cursor.fetchone()
		title = "ToroMovies | Profile"

		cursor2 = mydb.cursor()
		sql2 = "SELECT * FROM genres"
		cursor.execute(sql2)
		categories = cursor.fetchall()

		cursor3 = mydb.cursor()
		sql3 = "SELECT * FROM years"
		cursor.execute(sql3)
		years = cursor.fetchall()

		return render_template('profile.html', user=user, title=title, pelicula="", categories=categories, years=years)
	else:
		return redirect(url_for('users.login'))
@users.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('users.login'))
