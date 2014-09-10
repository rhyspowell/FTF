# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy

# create our little application
app = Flask(__name__)
#application configuration
app.config.from_pyfile('blogger.config')
db = SQLAlchemy(app)

class Authors(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	name = db.Column(db.String(64))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return'<Authors %r>' % self.name

class Entries(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	title = db.Column(db.String(128))
	text = db.Column(db.Text)
	published = db.Column(db.Boolean)
	author = db.Column(db.Integer, db.ForeignKey('authors.id'))
	published_time = db.Column(db.DateTime)

	def __init__(self, title, text, author, published_time=None):
		self.title = title
		self.text = text
		if published_time is None:
			published_time = datetime.utcnow()
		self.published_time = published_time
		self.author = author

	def __repr__(self):
		return '<Post %r>' % self.title

#main page route
@app.route('/')
def show_entries():
	#cur = g.db.execute('select title, text from entries order by id desc')
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	#cur = g.db.execute('select name, url from menu')
	#menu_items = [dict(name=row[0], url=row[1]) for row in cur.fetchall()]
	entries = Entries.query.all()
	return render_template('show_entries.html', entries=entries)

#add an author
@app.route('/add-author', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		if not session.get('logged_in'):
			flash('You need to be logged in to do that')
			return redirect(url_for('show_entries'))
		return render_template('add_author.html')
	if request.method =='POST':
		author = Authors(request.form['name'])
		db.session.add(author)
		db.session.commit()
		flash('New author aded to the list')
		return redirect(url_for('show_entries'))

#add a post
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
	if request.method == 'GET':
		if not session.get('logged_in'):
			flash('You need to be logged in to do that')
			return redirect(url_for('show_entries'))
		return render_template('add_post.html')
	if request.method == 'POST':
		g.db.execute('insert into entries (title, text) values (?,?)', [request.form['title'], request.form['text']])
		g.db.commit()
		flash('New entry was sucessfully posted')
		return redirect(url_for('show_entries'))

#login and out methods
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = "Incorrect username or password"
		else:
			session['logged_in'] = True
			flash('You have sucessfully logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You have been logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()
