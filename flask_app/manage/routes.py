from flask import render_template, url_for, request, redirect, flash, send_from_directory, Blueprint
from datetime import datetime, date, timedelta
from flask_app import db
from flask_app.models import Devotional, Calendar, Announcement, User, UserMessages, Application
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

manage = Blueprint('manage', __name__,
                    template_folder='templates') 

db_name_to_object = {
    'Calendar': Calendar, 
    'Devotional': Devotional, 
    'Announcment': Announcement,
    'User' : User
    }

name_to_symbol ={
    'Mythic+': '/static/main/img/m-plus-icon.png', 
    'Devotionals':'/static/main/img/devo-icon.png',
    'Progression Raid':'/static/main/img/p-raid-icon.png', 
    'Casual Raid':'/static/main/img/c-raid-icon.png',
    'Other': '/static/main/img/other-icon.png' 
    }

@manage.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    today = datetime.now() - timedelta(hours=6)
    devotionals = Devotional.query.order_by(Devotional.date.desc()).limit(3)
    events = Calendar.query.filter(Calendar.date >= today).order_by(Calendar.date.asc()).limit(7)
    announcements = Announcement.query.all()
    numb_of_applicants = 0
    return render_template('manage_index.html', devotionals=devotionals, events=events, announcements=announcements, applicants=numb_of_applicants)


@manage.route('/announcements')
@login_required
def manage_announcements():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_announcements = Announcement.query.all()
    return render_template('manage_announcements.html', announcements=all_announcements)


@manage.route('/events')
@login_required
def manage_events():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_events = Calendar.query.order_by(Calendar.date.desc()).all()
    return render_template('manage_events.html', events=all_events)


@manage.route('/devotionals')
@login_required
def manage_devotionals():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_devotionals = Devotional.query.order_by(Devotional.date.desc()).all()
    return render_template('manage_devotionals.html', devotionals=all_devotionals)


@manage.route('/applications', methods=['GET', 'POST'])
@login_required
def manage_applications():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        if request.form['approve'] == "True":
            user = User.query.get(request.form['user_id'])
            user.rank = request.form['rank']
            user.application.status = "Approved"
            ##### message #####
            from_user = request.form['from_user']
            message_title = "Welcome aboard!"
            message_body = "Welcome, we are glad to have you join us here. We have several ways to keep up with all the happenings in the guild. \
            The calendar here on the website lists fun activities and event schedules. We have an active Facebook group (search for “Renewed Hope ¬ World of Warcraft Guild”, and apply). \
           Discord is our main voice and messaging system (https://discord.gg/4b5Bxh). \nIf you ever need anything don’t hesitate to ask any of our fine officers or friendly guild mates. \n\nWarmest welcome " + user.application.name
            user_id = request.form['user_id']
            approve_message = UserMessages(from_user=from_user, message_title=message_title, message_body=message_body, user_id=user_id)
            try:
                db.session.commit()
                db.session.add(approve_message)
                db.session.commit()
                flash("The application has been approved and a message was sent to the user!", "success")
                return redirect(url_for('manage.manage_applications'))
            except:
                flash("There was a problem approving this application. Please try again later", "danger")
                return redirect(url_for('manage.manage_applications'))
        elif request.form['approve'] == "False":
            user = User.query.get(request.form['user_id'])
            user.rank = 11
            user.application.status = "Rejected"
            ##### message #####
            from_user = request.form['from_user']
            message_title = "Thanks for applying"
            message_body = "We’re terribly sorry but we are passing on your application. Not everyone would be a good fit for Renewed Hope and we sincerely hope that you find a guild that is perfect for you and your needs.\n\nThank you for your interest."
            user_id = request.form['user_id']
            approve_message = UserMessages(from_user=from_user, message_title=message_title, message_body=message_body, user_id=user_id)
            try:
                db.session.commit()
                db.session.add(approve_message)
                db.session.commit()
                flash("The application has been rejected and a message was sent to the user!", "success")
                return redirect(url_for('manage.manage_applications'))
            except:
                flash("There was a problem rejecting this application. Please try again later", "danger")
                return redirect(url_for('manage.manage_applications'))

            flash("The request.get('approve') was not = to 'True'", "danger")
            return redirect(url_for('manage.manage_applications'))

    applications = User.query.filter(User.application).all()
    return render_template('manage_applications.html', applications=applications)





rank_list = ["Web-Admin", "GM", "Assistant-GM", "Recruitment-Officer", "Officer", "Member", "Member", "Initiate", "Applicant", "Registered", "Rejected"]


@manage.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        database = db_name_to_object[request.form['db']]
        user_to_update = database.query.get_or_404(request.form['id'])
        user_to_update.username = request.form['username']
        user_to_update.rank = (rank_list.index(request.form['rank']) + 1)
        try:
            db.session.commit()
            flash("The User was successfully updated!")
            return redirect('/manage_users')
        except:
            flash("I was not able to update that user!", 'danger')
            return redirect('/manage_users')
        
            

    else:
        user_messages = UserMessages.query.order_by(UserMessages.message_date.desc()).all()
        users = User.query.filter(User.rank > current_user.rank)
        return render_template('manage_users.html', users=users, rank_list=rank_list, user_messages=user_messages)


@manage.route('/search', methods=['POST'])
@login_required
def search():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    search = request.form['search']
    database = db_name_to_object[request.form['db']]
    results = database.query.filter(or_(database.title.like('%' + search + '%'), database.description.like('%' + search + '%')))
    data = results.count()
    return render_template('results.html', results=results, search=request.form['search'], db=request.form['db'], data=data )
 

@manage.route('/update', methods=['POST'])
@login_required
def update():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
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
        event_to_update.lead = request.form['lead']

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
@login_required
def insert():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
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
        lead = request.form['lead']
        if int(request.form['n-times']) == 0:
            new_event = Calendar(title=title, date=date, time=time, description=description, symbol=symbol, lead=lead)
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
@login_required
def delete():
    if current_user.rank > 5 and current_user.id == request.form['id']:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
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
            flash("Announcement was deleted successfully!", "success")
            return redirect('/announcements')
        except:
            return "There was a problem deleting this announcement. Please go back!"
    elif request.form['db'] == 'Calendar':
        event_to_delete = Calendar.query.get_or_404(request.form['id'])
        try:
            db.session.delete(event_to_delete)
            db.session.commit()
            flash("Event was deleted successfully!", "success")
            return redirect('/events')
        except:
            return "There was a problem deleting this event. Please go back!"
    elif request.form['db'] == 'Devotional':
        devotional_to_delete = Devotional.query.get_or_404(request.form['id'])
        try:
            db.session.delete(devotional_to_delete)
            db.session.commit()
            flash("Devotional was deleted successfully!", "success")
            return redirect('/devotionals')
        except:
            return "There was a problem deleting this devotional. Please go back!"
    elif request.form['db'] == 'User':
        user_to_delete = User.query.get_or_404(request.form['id'])
        try:            
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User was deleted successfully!", "success")
            return redirect('/manage_users')
        except:
            return "There was a problem deleting this User. Please go back!"
    # elif request.form['db'] == 'User':
    #     user_to_delete = User.query.get_or_404(request.form['id'])
    #     try:
    #         if user_to_delete.application == None:
    #             pass
    #         elif user_to_delete.application.note != "None":
    #             note = user_to_delete.application.note
    #             note += " Note: Accounted deleted on: " + str(datetime.utcnow()) + "first if"
    #             user_to_delete.application.note = note
    #         elif user_to_delete.application.note == "None":
    #             user_to_delete.application.note = " Note: Accounted deleted on: " + str(date.today()) + " Second if"
    #         else:
    #             print("There was no application")
            
    #         db.session.delete(user_to_delete)
    #         db.session.commit()
    #         flash("User was deleted successfully!", "sucess")
    #         return redirect('/manage_users')
    #     except:
            # return "There was a problem deleting this User. Please go back!"
    return redirect('/admin')

