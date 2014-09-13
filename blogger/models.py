from flask.ext.sqlalchemy import SQLAlchemy
'''
Note that we have not initialized our flask.ext.sqlalchemy object
with any application so these models are not bound to this
particular application (this flexibility comes with some
small costs, which we will encounter shortly).
'''

db = SQLAlchemy()

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

	#Normally SQLAlchemy would use the class name by default
	#this can be overridden using below
	__tablename__ = 'entries'

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

	#This will give better information should the command be
	#run via cli
	def __repr__(self):
		return '<Post %r>' % self.title

class Menu_Items(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
	title = db.Column(db.String(30))
	url = db.Column(db.String(250))

	def __init__(self, title, url):
		self.title = title
		self.url = url

	#This will give better information should the command be
	#run via cli
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