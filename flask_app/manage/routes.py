from flask import render_template, url_for, request, redirect, flash, send_from_directory, Blueprint
from datetime import datetime, date, timedelta
from flask_app import db
from flask_app.models import Devotional, Calendar, Announcement
from flask_login import current_user
from sqlalchemy import and_, or_

manage = Blueprint('manage', __name__,
                    template_folder='templates') 

db_name_to_object = {
    'Calendar': Calendar, 
    'Devotional': Devotional, 
    'Announcment': Announcement
    }

name_to_symbol ={
    'Mythic+': '/static/main/img/m-plus-icon.png', 
    'Devotionals':'/static/main/img/devo-icon.png',
    'Progression Raid':'/static/main/img/p-raid-icon.png', 
    'Casual Raid':'/static/main/img/c-raid-icon.png',
    'Other': '/static/main/img/other-icon.png' 
    }

@manage.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        pass
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        today = date.today()
        devotionals = Devotional.query.order_by(Devotional.date.desc()).limit(3)
        events = Calendar.query.filter(Calendar.date >= today).order_by(Calendar.date.asc()).limit(7)
        announcements = Announcement.query.all()
        numb_of_applicants = 0
        return render_template('manage_index.html', devotionals=devotionals, events=events, announcements=announcements, applicants=numb_of_applicants)


@manage.route('/announcements')
def manage_announcements():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
 
    all_announcements = Announcement.query.all()
    return render_template('manage_announcements.html', announcements=all_announcements)


@manage.route('/events')
def manage_events():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    all_events = Calendar.query.order_by(Calendar.date.desc()).all()
    return render_template('manage_events.html', events=all_events)


@manage.route('/devotionals')
def manage_devotionals():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    all_devotionals = Devotional.query.order_by(Devotional.date.desc()).all()
    return render_template('manage_devotionals.html', devotionals=all_devotionals)


@manage.route('/search', methods=['POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    search = request.form['search']
    database = db_name_to_object[request.form['db']]
    results = database.query.filter(or_(database.title.like('%' + search + '%'), database.description.like('%' + search + '%')))
    data = results.count()
    return render_template('results.html', results=results, search=request.form['search'], db=request.form['db'], data=data )
 

@manage.route('/update', methods=['POST'])
def update():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    
    if request.form['db'] == 'Announcement':
        announcement_to_update = Announcement.query.get_or_404(request.form['id'])
        announcement_to_update.title = request.form['title']
        announcement_to_update.description = request.form['description']
        announcement_to_update.link = request.form['link']
        try:
            db.session.commit()
            flash("The Announcement was successfully updated!")
            return redirect('/announcements')
        except:
            return "There was an issue updating this record. Please go back!"

    elif request.form['db'] == 'Calendar':
        event_to_update = Calendar.query.get_or_404(request.form['id'])
        event_to_update.title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        event_to_update.date = date
        event_to_update.time = request.form['time']
        event_to_update.description = request.form['description']
        event_to_update.symbol = name_to_symbol[request.form['symbol']]

        try:
            db.session.commit()
            flash("The Event was successfully updated!")
            return redirect('/events')
        except:
            return "There was an issue updating this record. Please go back!"

    elif request.form['db'] == 'Devotional':
        devotional_to_update = Devotional.query.get_or_404(request.form['id'])
        devotional_to_update.title = request.form['title']
        date = request.form['date']
        devotional_to_update.date = date
        devotional_to_update.content = request.form['content']
        devotional_to_update.download_link = request.form['download_link']
        devotional_to_update.date_updated = datetime.utcnow()
        devotional_to_update.lead = request.form['lead']

        try:
            db.session.commit()
            flash("The Devotional was successfully updated!")
            return redirect('/devotionals')
        except:
            return "There was an issue updating this record. Please go back!"

    return redirect('/admin')


@manage.route('/insert', methods=['POST'])
def insert():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    # Refactor this to use the db
    if request.form['db'] == 'Announcement':
        title = request.form['title']
        description = request.form['description']
        link = request.form['link']
        new_announcement = Announcement(title=title, description=description, link=link)        
        try:
            db.session.add(new_announcement)
            db.session.commit()
            flash("The Announcement was successfully added!")
            return redirect('/announcements')
        except:
            return "There was an issue updating this announcement :("

    elif request.form['db'] == 'Calendar':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        time = request.form['time']
        description = request.form['description']
        symbol = name_to_symbol[request.form['symbol']]
        if int(request.form['n-times']) == 0:
            new_event = Calendar(title=title, date=date, time=time, description=description, symbol=symbol)
            try:
                db.session.add(new_event)
                db.session.commit()
                flash("The Event was successfully added!")
                return redirect('/events')
            except:
                return "There was an issue adding this event. Please go back!"
        else:
            repeat_num_days = int(request.form['n-days'])
            repeat_num_times = int(request.form['n-times'])
            repeat_delta = timedelta(days=repeat_num_days)
            for _ in range(repeat_num_times):
                new_event = Calendar(title=title, date=date, time=time, description=description, symbol=symbol)
                try:
                    db.session.add(new_event)
                    db.session.commit()
                except:
                    return "There was a problem adding this to the database :("
                date += repeat_delta
            flash("All events were successfully added!")
            return redirect('/events')


    elif request.form['db'] == 'Devotional':
        date = request.form['date']
        split_date = date.split('-')
        title = 'Devotionals for ' + split_date[1] + "-" + split_date[2] + "-" + split_date[0]
        content = request.form['content']
        download_link = request.form['download_link']
        lead = request.form['lead']
        new_devotional = Devotional(title=title, date=date, content=content, download_link=download_link, lead=lead)
        try:
            db.session.add(new_devotional)
            db.session.commit()
            flash("The Devotional was successfully added!")
            return redirect('/devotionals')
        except:
            return "There was an issue adding this devotional. Please go back!"
    return redirect('/admin')

@manage.route('/delete', methods=['POST'])
def delete():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    if request.form['search'] != "False":
        items_to_delete = request.form['search']
        database = db_name_to_object[request.form['db']]
        results = database.query.filter(or_(database.title.like('%' + items_to_delete + '%'), database.description.like('%' + items_to_delete + '%')))
        for result in results:
            item_to_delete = database.query.get_or_404(result.id)
            try:
                db.session.delete(item_to_delete)
                db.session.commit()
            except:
                return "There was an issue deleting this item :("
        flash("All search results were successfully deleted!")
        return redirect('/events')
    

    # refactor this like the results page
    if request.form['db'] == 'Announcement':
        announcement_to_delete = Announcement.query.get_or_404(request.form['id'])
        try:
            db.session.delete(announcement_to_delete)
            db.session.commit()
            flash("Announcement was deleted successfully!")
            return redirect('/announcements')
        except:
            return "There was a problem deleting this announcement. Please go back!"
    elif request.form['db'] == 'Calendar':
        event_to_delete = Calendar.query.get_or_404(request.form['id'])
        try:
            db.session.delete(event_to_delete)
            db.session.commit()
            flash("Event was deleted successfully!")
            return redirect('/events')
        except:
            return "There was a problem deleting this event. Please go back!"
    elif request.form['db'] == 'Devotional':
        devotional_to_delete = Devotional.query.get_or_404(request.form['id'])
        try:
            db.session.delete(devotional_to_delete)
            db.session.commit()
            flash("Devotional was deleted successfully!")
            return redirect('/devotionals')
        except:
            return "There was a problem deleting this devotional. Please go back!"
    return redirect('/admin')

