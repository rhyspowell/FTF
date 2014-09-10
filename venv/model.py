from app import db
class Authors(db.Model):
	id = db.Column(db.Interger, primary_key = True autoincrement=True,
	name = db.Column(db.String(64) not_null = True