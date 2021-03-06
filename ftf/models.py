import datetime
from random import SystemRandom

from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from ftf.data import CRUDMixin, db


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))
    #sites = db.relationship('Site', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    # In order to ensure that passwords are always stored
    # hashed and salted in our database we use a descriptor
    # here which will automatically hash our password
    # when we provide it (i. e. user.password = "12345")
    @password.setter
    def password(self, value):
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """Ensure that the provided password is valid.

        We are using this instead of a ``sqlalchemy.types.TypeDecorator``
        (which would let us write ``User.password == password`` and have the incoming
        ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all***
        the characters of the hash even when they do not match in order to
        avoid timing oracle side-channel attacks."""
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
        return bytes(buff)

    def __repr__(self):
        return "<User #{:d}>".format(self.id)

class Entries(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True,)
    title = db.Column(db.String(128))
    postlink = db.Column(db.String(128))
    text = db.Column(db.Text)
    status = db.Column(db.Boolean)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    publishedtime = db.Column(db.DateTime)

    #def __init__(self, title, text, author, published_time=None):
    #    self.title = title
    #    self.text = text
    #    if published_time is None:
    #        published_time = datetime.utcnow()
    #    self.published_time = published_time
    #    self.author = author

    def __init__(self, title, text, status, publishedtime, author=None ):
        self.title = title
        self.text = text
        self.status = status
        if self.author is None:
            self.author = 1
        if publishedtime == '':
            self.publishedtime = datetime.datetime.utcnow()
        else:
            self.publishedtime = publishedtime
        self.postlink = title.replace(" ", "-")

    def __repr__(self):
        return '<Post %r>' % self.title

class MenuItems(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(128))

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Post %r>' % self.name
