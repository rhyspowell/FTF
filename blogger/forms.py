from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import User

class AddUserForm(Form):
	username = fields.StringField()
	password = fields.PasswordField()
	email = fields.StringField()
	#role

class Roles(Form):
	role = fields.SelectField()

class AddEntry(Form):
	title = fields.StringField()
	text = fields.TextField()
	published = fields.BooleanField()
	author = QuerySelectField(query_factory=lambda: User.query.all())