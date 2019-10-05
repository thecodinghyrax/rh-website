from flask import Blueprint, request, send_from_directory, render_template, redirect, url_for, flash
from flask_app import app, db, bcrypt
from flask_app.models import Devotional, News, Calendar, User
import os, calendar
from datetime import date
from sqlalchemy import extract
from flask_login import current_user, login_user, logout_user
from flask_app.main.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)

@main.route('/robots.txt')
@main.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@main.route('/')
def index():
    devotional = Devotional.query.order_by(Devotional.date.desc()).first()
    news = News.query.order_by(News.id.asc()).all()
    return render_template('index.html', devotional=devotional, news=news)

@main.route('/sitemap')
def sitemap():
    return render_template('sitemap.xml')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@main.route('/guild_calendar')
def guild_calendar():
    today = date.today()
    year = today.year
    current_month = today.month
    month = today.month
    if request.args.get('year'):
        year = int(request.args.get('year'))
    if request.args.get('month'):
        month = int(request.args.get('month'))
        if month < 1:
            month = 12
            year = year - 1
        elif month > 12:
            month = 1
            year = year + 1
    # if month < 10:
    #     year_plus_month = str(year) + "-0" + str(month)
    # else:
    #     year_plus_month = str(year) + "-" + str(month)
    # events = Event.query.filter(Event.date.startswith(year_plus_month)).all()
    events = Calendar.query.filter(extract('month', Calendar.date) == month, extract('year', Calendar.date) == year).all()#and_(Calendar.date.year == year, Calendar.date.month == month)).all()
    # current_day = int(today.strftime('%d'))
    current_day = today.day
    month_name = calendar.month_name[month]
    cal = calendar.Calendar()
    cal.setfirstweekday(calendar.SUNDAY)
    current_cal = cal.monthdayscalendar(year, month)
    if len(current_cal) < 6:
        extra_week = [[0,0,0,0,0,0,0]]
        current_cal = current_cal + extra_week

    return render_template('calendar.html', cal=current_cal, month=month, month_name=month_name, current_month=current_month, year=year, events=events, current_day=current_day)

@main.route('/discord')
def discord():
    return render_template('discord.html')

@main.route('/devotional')
def devotionals():
    page = request.args.get('page', 1, type=int)
    devotionals = Devotional.query.order_by(Devotional.date.desc()).paginate(page=page, per_page=20)

    return render_template('devotional.html', devotionals=devotionals)

@main.route('/about')
def about():
    return render_template('about.html')

# @main.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Your account has been created and you are now able to login', 'success')
#         return redirect(url_for('main.login'))

#     return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('manage.admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))