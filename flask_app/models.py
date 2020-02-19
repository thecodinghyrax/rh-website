from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Devotional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(40), nullable=False)
    content = db.Column(db.Text, nullable=False)
    download_link = db.Column(db.String(1000), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    lead = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"Devotional('{self.id}', '{self.title}', '{self.date}')"
        # return '<Devotional %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    lead = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Calendar('{self.title}', '{self.date}', '{self.time}', '{self.description}', {self.symbol}, {self.lead})"

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anchor = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"News('{self.id}', '{self.anchor}')"

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"Calendar('{self.title}', '{self.description}', '{self.link}')"