from flask import render_template, url_for, request, redirect, flash, send_from_directory, Blueprint
from datetime import datetime, date, timedelta
from flask_app import db
from flask_app.models import Devotional, Calendar, Announcement
from flask_login import current_user
from sqlalchemy import and_, or_

manage = Blueprint('manage', __name__,
                    template_folder='templates') 


@manage.route('/add_devotional', methods=['POST', 'GET'])
def add_devotional():
    if request.method == 'POST':
        date = request.form['date']
        split_date = date.split('-')
        description = request.form['description']
        link = request.form['link']
        title = 'Devotionals for ' + split_date[1] + "-" + split_date[2] + "-" + split_date[0]
        lead = request.form['lead']
        new_devotional = Devotional(title=title, date=date, content=description, download_link=link, lead=lead)
        try:
            db.session.add(new_devotional)
            db.session.commit()
            return redirect('/add_devotional')
        except:
            return "There was a problem adding this to the database :("
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        devotionals = Devotional.query.order_by(Devotional.date.desc()).all()
        return render_template('add_devotional.html', devotionals=devotionals)


@manage.route('/delete')
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
        elif confirm_type == "Announcement":
            item_to_delete = Announcement.query.get_or_404(id)
            try:
                db.session.delete(item_to_delete)
                db.session.commit()
                return redirect('/admin')
            except:
                return "There was an issue deleting the announcement :("
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


@manage.route('/confirm')
def confirm():
    if request.args.get('id'):
        confirm_type = request.args.get('confirm_type')
        id = request.args.get('id')
        if confirm_type == "Devotional":
            item_to_delete = Devotional.query.get(id)
        elif confirm_type == "Event":
            item_to_delete = Calendar.query.get(id)
        elif confirm_type == "Announcement":
            item_to_delete = Announcement.query.get(id)
        return render_template('confirm.html', id=id, item_to_delete=item_to_delete, confirm_type=confirm_type)
    elif request.args.get('delete'):
        search = request.args.get('delete')
        events = Calendar.query.filter(or_(Calendar.title.like('%' + search + '%'), Calendar.description.like('%' + search + '%')))
        return render_template('confirm.html', events_to_delete=events, search=search)
    else:
        pass


@manage.route('/devotional_update/<int:id>', methods=['GET', 'POST'])
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

@manage.route('/event_update/<int:id>', methods=['GET', 'POST'])
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
            return redirect('/admin')
        except:
            return "There was an issue updating this event :("
    else:
        return render_template('event_update.html', event=event_to_update)

@manage.route('/announcement_update/<int:id>', methods=['GET', 'POST'])
def announcement_update(id):
    announcement_to_update = Announcement.query.get_or_404(id)
    if request.method == 'POST':
        announcement_to_update.title = request.form['title']
        announcement_to_update.description = request.form['description']
        announcement_to_update.link = request.form['link']

        try:
            db.session.commit()
            return redirect('/admin')
        except:
            return "There was an issue updating this event :("
    else:
        return render_template('announcement_update.html', announcement=announcement_to_update)


@manage.route('/add_event', methods=['POST', 'GET'])
def add_event():
    if request.method == 'POST':
        print(request.get_data())
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
            return redirect(url_for('main.login'))
        page = request.args.get('page', 1, type=int)
        event = Calendar.query.order_by(Calendar.date.desc()).paginate(page=page, per_page=20)
        return render_template('add_event.html', event=event)

@manage.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        pass
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        today = date.today()
        devotionals = Devotional.query.order_by(Devotional.date.desc()).limit(5)
        events = Calendar.query.filter(Calendar.date >= today).order_by(Calendar.date.asc()).limit(7)
        announcements = Announcement.query.all()
        return render_template('admin.html', devotionals=devotionals, events=events, announcements=announcements)

@manage.route('/results/')
def results():
    if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
    # event_search = request.args.get('event')
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

@manage.route('/add_announcement', methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        link = request.form['link']
        new_announcement = Announcement(title=title, description=description, link=link)
        try:
            db.session.add(new_announcement)
            db.session.commit()
            return redirect('/admin')
        except:
            return "There was a problem adding this to the database :("
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        announcements = Announcement.query.all()
        return render_template('add_announcement.html', announcements=announcements)
