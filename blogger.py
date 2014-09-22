# all the imports
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy, Pagination

# create our little application
app = Flask(__name__)
#application configuration
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

#flask-login start
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


#lets get all the database built
ROLE_USER = 0
ROLE_ADMIN = 1
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Entries(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	title = db.Column(db.String(128))
	text = db.Column(db.Text)
	published = db.Column(db.Boolean)
	author = db.Column(db.Integer, db.ForeignKey('user.id'))
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

class Menu_Items(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	title = db.Column(db.String(30))
	url = db.Column(db.String(250))

	def __init__(self, title, url):
		self.title = title
		self.url = url

	def __repr__(self):
		return'<Title %r>' %self.title

class Sections(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	title = db.Column(db.String(30))
	page = db.Column(db.String(250))

	def __init__(self, title, page):
		self.title = title
		self.url = url

	def __repr__(self):
		return'<Title %r>' %self.title

#Drop all the admin stuff in first
#view admin page
@app.route('/admin')
@login_required
def admin():
	sections = Sections.query.all()
	return render_template('/admin/admin.html', sections=sections)

@app.route('/admin/add-section')
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
@app.route('/admin/add-author', methods=['GET', 'POST'])
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

#main page route
@app.route('/')
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

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You have been logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()
