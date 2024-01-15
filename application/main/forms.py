from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please chose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email address is taken. Please chose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please chose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email address is taken. Please chose another one.')

class ApplyToGuildForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    join_how = RadioField('How will you be joining us?', choices=[('Already on the server', 'Already on the server'), ('Rolling a new toon', 'Rolling a new toon'), ('Transfering a toon', 'Transfering a toon')], validators=[DataRequired()])
    find_how = RadioField('How did you find us?', choices=[('Google', 'Google'), ('Forum post', 'Forum post'), ('Friend Refered', 'Friend Refered'), ('Other', 'Other')], validators=[DataRequired()])
    self_description = TextAreaField('Describe yourself and what your looking for in a guild', validators=[DataRequired()])
    b_tag = StringField('Battle Tag')
    have_auth = RadioField('Do you have a Blizzard Authenticator enabled on your account?', choices=[('Yes', 'Yes'), ('No', 'No'), ('I\'m not sure', 'I\'m not sure')], validators=[DataRequired()])
    play_when = StringField('What times do you play?', validators=[DataRequired()])
    submit = SubmitField('Submit Application')
