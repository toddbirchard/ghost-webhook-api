"""Data model for BuyMeACoffee donations."""
from sqlalchemy.ext.declarative import declarative_base
from api import db

Base = declarative_base()


class Donation(db.Model):
	"""Data model example."""
	__tablename__ = 'donations'
	__bind_key__ = 'donations'

	id = db.Column(
		db.Integer,
		primary_key=True,
		index=True,
		nullable=False,
		autoincrement=True,
		unique=True
	)
	email = db.Column(
		db.String(255),
		nullable=False,
	)
	name = db.Column(
		db.String(255),
		nullable=True
	)
	count = db.Column(
		db.Integer,
		nullable=False
	)
	message = db.Column(
		db.Text,
		nullable=True
	)
	link = db.Column(
		db.String(255),
		nullable=True
	)
	coffee_id = db.Column(
		db.Integer,
		unique=True,
		nullable=True
	)
	created_at = db.Column(
		db.Date,
		nullable=False,
		server_default=db.text('CURDATE()')
	)

	def __repr__(self):
		return '<Donations model {}>'.format(self.id)

