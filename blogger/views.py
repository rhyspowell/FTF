from flask import Blueprint, flash, Markup, redirect, render_template, url_for

from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required

from .forms import AddUserForm, Roles, AddEntry
from .models import db, User, Entries, Menu_Items, Sections

blogger = Blueprint("blogger", __name__)

#flask-login start
lm = LoginManager()
lm.init_app(blogger)
lm.login_view = 'login'

#Drop all the admin stuff in first
#view admin page
@blogger.route('/admin')
@login_required
def admin():
	sections = Sections.query.all()
	return render_template('/admin/admin.html', sections=sections)

@blogger.route('/admin/add-section')
@login_required
def add_section():
	if request.method == 'GET':
		return render_template('admin/add_author.html')
	if request.method =='POST':
		author = Authors(request.form['name'])
		db.session.add(author)
		db.session.commit()
		flash('New author aded to the list')
		return redirect(url_for('show_entries'))

#add an author
@blogger.route('/admin/add-author', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		if not session.get('logged_in'):
			flash('You need to be logged in to do that')
			return redirect(url_for('show_entries'))
		return render_template('admin/add_author.html')
	if request.method =='POST':
		author = Authors(request.form['name'])
		db.session.add(author)
		db.session.commit()
		flash('New author aded to the list')
		return redirect(url_for('show_entries'))

#add a post
@blogger.route('/add', methods=['GET', 'POST'])
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

#main page route
@blogger.route('/')
def show_entries():
	#cur = g.db.execute('select title, text from entries order by id desc')
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	#cur = g.db.execute('select name, url from menu')
	#menu_items = [dict(name=row[0], url=row[1]) for row in cur.fetchall()]
	entries = Entries.query.all()
	menu_items = Menu_Items.query.all()
	return render_template('show_entries.html', entries=entries, menu_items=menu_items)

#login and out methods
@lm.user_loader
def load_user(userid):
	return User.get(userid)

@blogger.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	username = request.form['username']
	password = request.form['password']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		flash('Username or Password is invalid' , 'error')
		return redirect(url_for('login'))
	#login_user(registered_user)
	flash('Logged in successfully')
	return redirect(request.args.get('next') or url_for('show_entries'))

@blogger.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You have been logged out')
	return redirect(url_for('show_entries'))
