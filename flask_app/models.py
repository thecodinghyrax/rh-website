from datetime import datetime
from flask_app import db

class Devotional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    download_link = db.Column(db.String(1000), nullable=False)
    date_updated = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return '<Devotional %r>' % self.id
