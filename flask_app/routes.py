from flask import render_template, url_for, request, redirect, flash, send_from_directory
from flask_app import app, db, bcrypt
from flask_app.models import Devotional, User, Calendar, News
from forms import RegistrationForm, LoginForm
from datetime import date, datetime, timedelta
from flask_login import login_user, current_user, logout_user
from sqlalchemy import and_, or_, extract
import os, calendar 

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

###################################################################################
# Public pages
###################################################################################

@app.route('/')
def index():
    devotional = Devotional.query.order_by(Devotional.date.desc()).first()
    news = News.query.order_by(News.id.asc()).all()
    return render_template('index.html', devotional=devotional, news=news)

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.xml')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/guild_calendar')
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
    # events = Event.query.order_by(Event.title).all()
    if month < 10:
        year_plus_month = str(year) + "-0" + str(month)
    else:
        year_plus_month = str(year) + "-" + str(month)
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

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/devotional')
def devotionals():
    page = request.args.get('page', 1, type=int)
    devotionals = Devotional.query.order_by(Devotional.date.desc()).paginate(page=page, per_page=20)

    return render_template('devotional.html', devotionals=devotionals)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'Your account has been created and you are now able to login', 'success')
#         return redirect(url_for('login'))

#     return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

###################################################################################
# Backend pages
###################################################################################

@app.route('/add_devotional', methods=['POST', 'GET'])
def add_devotional():
    if request.method == 'POST':
        date = request.form['date']
        split_date = date.split('-')
        description = request.form['description']
        link = request.form['link']
        title = 'Devotionals for ' + split_date[1] + "-" + split_date[2] + "-" + split_date[0]
        lead = request.form['lead']
        date_updated = datetime.utcnow()
        new_devotional = Devotional(title=title, date=date, content=description, download_link=link, lead=lead)
        try:
            db.session.add(new_devotional)
            db.session.commit()
            return redirect('/add_devotional')
        except:
            return "There was a problem adding this to the database :("
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        devotionals = Devotional.query.order_by(Devotional.date.desc()).all()
        return render_template('add_devotional.html', devotionals=devotionals)


@app.route('/delete')
def delete():
    if request.args.get('confirm_type'):
        confirm_type = request.args.get('confirm_type')
        id = request.args.get('id')
        if confirm_type == "Devotional":
            item_to_delete = Devotional.query.get_or_404(id)
            try:
                db.session.delete(item_to_delete)
                db.session.commit()
                return redirect('/add_devotional')
            except:
                return "There was an issue deleting the devotional :("
        elif confirm_type == "Event":
            item_to_delete = Calendar.query.get_or_404(id)
            try:
                db.session.delete(item_to_delete)
                db.session.commit()
                return redirect('/add_event')
            except:
                return "There was an issue deleting the devotional :("
        else:
            return '''There was a problem deleting this record. Please go back!'''
    elif request.args.get('all'):
        search = request.args.get('all')
        events = Calendar.query.filter(or_(Calendar.title.like('%'+search+'%'), Calendar.description.like('%'+search+'%')))
        for event in events:
            item_to_delete = Calendar.query.get_or_404(event.id)
            try:
                db.session.delete(item_to_delete)
                db.session.commit()
            except:
                return "There was an issue deleting the devotional :("
        return redirect('/admin')
    else:
        return "There was an issue deleting the thing :("


@app.route('/confirm')
def confirm():
    if request.args.get('id'):
        confirm_type = request.args.get('confirm_type')
        id = request.args.get('id')
        if confirm_type == "Devotional":
            item_to_delete = Devotional.query.get(id)
        elif confirm_type == "Event":
            item_to_delete = Calendar.query.get(id)
        # devotional = Devotional.query.get(id)
        return render_template('confirm.html', id=id, item_to_delete=item_to_delete, confirm_type=confirm_type)
    elif request.args.get('delete'):
        search = request.args.get('delete')
        events = Calendar.query.filter(or_(Calendar.title.like('%' + search + '%'), Calendar.description.like('%' + search + '%')))
        return render_template('confirm.html', events_to_delete=events, search=search)
    else:
        pass


@app.route('/devotional_update/<int:id>', methods=['GET', 'POST'])
def devotional_update(id):
    devotional_to_update = Devotional.query.get_or_404(id)
    if request.method == 'POST':
        devotional_to_update.title = request.form['title']
        devotional_to_update.lead = request.form['lead']
        devotional_to_update.date = request.form['date']
        devotional_to_update.content = request.form['description']
        devotional_to_update.download_link = request.form['link']
        devotional_to_update.date_updated = datetime.utcnow()

        try:
            db.session.commit()
            return redirect('/add_devotional')
        except:
            return "There was an issue updating this devotional :("
    else:
        return render_template('devotional_update.html', devotional=devotional_to_update)

@app.route('/event_update/<int:id>', methods=['GET', 'POST'])
def event_update(id):
    event_to_update = Calendar.query.get_or_404(id)
    if request.method == 'POST':
        event_to_update.title = request.form['title']
        event_to_update.time = request.form['time']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        event_to_update.date = date
        event_to_update.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/add_event')
        except:
            return "There was an issue updating this event :("
    else:
        return render_template('event_update.html', event=event_to_update)


@app.route('/add_event', methods=['POST', 'GET'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        time = request.form['time']
        form_date = request.form['date']
        event_date = date.fromisoformat(form_date)
        description = request.form['description']
        
        if request.form['n-days'] != '':
            repeat_num_days = int(request.form['n-days'])
            repeat_num_times = int(request.form['n-times'])
            repeat_delta = timedelta(days=repeat_num_days)
            for event in range(repeat_num_times):
                # new_event = Event(title=title, date=event_date, time=time, content=content)
                new_event = Calendar(title=title, date=event_date, time=time, description=description)
                try:
                    db.session.add(new_event)
                    db.session.commit()
                except:
                    return "There was a problem adding this to the database :("
                event_date = event_date + repeat_delta
            return redirect('/add_event')
        else:
            new_event = Calendar(title=title, date=event_date, time=time, description=description)
            try:
                db.session.add(new_event)
                db.session.commit()
                return redirect('/add_event')
            except:
                return "There was a problem adding this to the database :("
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        page = request.args.get('page', 1, type=int)
        event = Calendar.query.order_by(Calendar.date.desc()).paginate(page=page, per_page=20)
        # event = Event.query.order_by(Event.date.desc())
        return render_template('add_event.html', event=event)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        pass
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        today = date.today()
        devotionals = Devotional.query.order_by(Devotional.date.desc()).limit(5)
        events = Calendar.query.filter(Calendar.date >= today).order_by(Calendar.date.asc()).limit(7)
        # events = Event.query.filter(Event.date == str(today)).limit(5)
        # events = Scheduledevent.query.order_by(Scheduledevent.id).all()
        return render_template('admin.html', devotionals=devotionals, events=events)

@app.route('/results/')
def results():
    if not current_user.is_authenticated:
            return redirect(url_for('login'))
    event_search = request.args.get('event')
    if request.args.get('devo'):
        search = '%' + request.args.get('devo') + '%'
        devotionals = Devotional.query.filter(or_(Devotional.title.like(search), Devotional.content.like(search)))
        return render_template('results.html', devotionals=devotionals, search=search)
    elif request.args.get('event'):
        search = request.args.get('event')
        events = Calendar.query.filter(or_(Calendar.title.like('%' + search + '%'), Calendar.description.like('%' + search + '%')))
        return render_template('results.html', events=events, search=search)
    else:
        return '''There was an issue...Please go back! '''
