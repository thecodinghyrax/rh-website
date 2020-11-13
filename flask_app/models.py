from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_app import db, login_manager, app
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
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    rank = db.Column(db.Integer, nullable=False, default=9 )
    application = db.relationship('Application', back_populates="user", uselist=False)
    messages = db.relationship('UserMessages', back_populates='user')
    notes = db.relationship('Notes', back_populates='user')



    def get_reset_token(self, expires_sec=18000):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.rank}', '{self.application}', '{self.messages}')"


class UserMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(50), nullable=False)
    from_user_image = db.Column(db.String(50))
    message_date = db.Column(db.DateTime, default=datetime.utcnow)
    message_body = db.Column(db.String(2000), nullable=False)
    acknowledged = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='messages')
    has_read = db.Column(db.Boolean(), default=False)


    def __repr__(self):
        return f"User('{self.id}','{self.from_user}', '{self.from_user_image}', '{self.message_date}', '{self.user_id}', '{self.acknowledged}')"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(75), nullable=False)
    join_how = db.Column(db.String(50), nullable=False)
    find_how = db.Column(db.String(200), nullable=False)
    self_description = db.Column(db.String(2000), nullable=False)
    b_tag = db.Column(db.String(50))
    have_auth = db.Column(db.String(20), nullable=False)
    play_when = db.Column(db.String(1000), nullable=False)
    # status is for where in the application process this is?
    status = db.Column(db.String(50), nullable=False, default="Accepted")
    note = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="application")

    def __repr__(self):
        return f"Application('{self.name}', '{self.app_date}', '{self.user_id}', '{self.join_how}', {self.find_how}, \
                                {self.self_description}, '{self.b_tag}', '{self.status}', '{self.note}')"

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String(50), nullable=False)
    from_user_image = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(4000))
    note_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='notes')

    def __repr__(self):
        return f"Notes('{self.user_id}', '{self.from_user}', '{self.date_posted}', '{self.note}', '{self.note_type}')"

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
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
        return f"Announcement('{self.title}', '{self.description}', '{self.link}')"

class News_cast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    embed = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=True)


    def __repr__(self):
        return f"News_cast('{self.title}', '{self.date}', '{self.embed}', '{self.description}')"

class Twitter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(1000), nullable=False)
    post_text = db.Column(db.String(300), nullable=True)
    date = db.Column(db.String(100))

    def __repr__(self):
        return f"Twitter('{self.picture}', '{self.post_text}', '{self.date}')"


