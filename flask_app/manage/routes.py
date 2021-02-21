from flask import render_template, url_for, request, redirect, flash, send_from_directory, Blueprint
from datetime import datetime, date, timedelta
from flask_app import db
from flask_app.models import Devotional, Calendar, Announcement, User, UserMessages, Application, News_cast, Notes
from flask_login import current_user, login_required
from sqlalchemy import and_, or_
from sqlalchemy.orm import load_only
from math import floor

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
    applicants = Application.query.filter(Application.status == "Application recieved").order_by(Application.app_date.desc()).all()
    no_ack_query = UserMessages.query.filter(UserMessages.acknowledged == False).all()
    return render_template('manage_index.html', devotionals=devotionals, no_ack=no_ack_query, events=events, announcements=announcements, applicants=applicants)


@manage.route('/announcements')
@login_required
def manage_announcements():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_announcements = Announcement.query.all()
    return render_template('manage_announcements.html', announcements=all_announcements)

@manage.route('/news-casts')
@login_required
def manage_news_casts():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_news_casts = News_cast.query.order_by(News_cast.date.desc()).all()
    return render_template('manage_news_casts.html', all_news_casts=all_news_casts)



@manage.route('/events')
@login_required
def manage_events():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    pag_number = 15
    current_date = datetime.now()
    future_events = floor(Calendar.query.filter(Calendar.date > current_date).count() / pag_number)
    page = request.args.get('page', (future_events + 1), type=int)
    all_events = Calendar.query.order_by(Calendar.date.desc()).paginate(page=page, per_page=pag_number)
    return render_template('manage_events.html', events=all_events)


@manage.route('/devotionals')
@login_required
def manage_devotionals():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    all_devotionals = Devotional.query.order_by(Devotional.date.desc()).all()
    return render_template('manage_devotionals.html', devotionals=all_devotionals)


@manage.route('/applications', methods=['POST'])
@login_required
def manage_applications():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        if request.form['approve'] == "True":
            user = User.query.get_or_404(request.form['user_id'])
            user.rank = request.form['rank']
            user.application.status = "Approved"
            ##### message #####
            from_user = request.form['from_user']
            return_path = request.form['return']
            from_user_image = request.form['from_user_image']
            message_body = "Welcome aboard!\n\nWe are glad to have you join us here. We have several ways to keep up with all the happenings in the guild. \
            The calendar here on the website lists fun activities and event schedules. We have an active Facebook group (search for “Renewed Hope - World of Warcraft Guild”, and apply). \
           Discord is our main voice and messaging system (https://discord.gg/4b5Bxh). \nIf you ever need anything don’t hesitate to ask any of our fine officers or friendly guild mates. \n\nWarmest welcome " + user.application.name
            user_id = request.form['user_id']
            approve_message = UserMessages(from_user=from_user, from_user_image=from_user_image, message_body=message_body, user_id=user_id)
            try:
                db.session.commit()
                db.session.add(approve_message)
                db.session.commit()
                flash("The application has been approved and a message was sent to the user!", "success")
                return redirect(url_for(return_path, id=user_id))
            except:
                flash("There was a problem approving this application. Please try again later", "danger")
                return redirect(url_for(return_path, id=user_id))
        elif request.form['approve'] == "False":
            user = User.query.get(request.form['user_id'])
            user.rank = 10
            user.application.status = "Rejected"
            return_path = request.form['return']
            ##### message #####
            from_user = request.form['from_user']
            from_user_image = request.form['from_user_image']
            message_body = "Thanks for applying\nWe’re terribly sorry but we are passing on your application. Not everyone would be a good fit for Renewed Hope and we sincerely hope that you find a guild that is perfect for you and your needs.\n\nThank you for your interest."
            user_id = request.form['user_id']
            approve_message = UserMessages(from_user=from_user, from_user_image=from_user_image, message_body=message_body, user_id=user_id)
            try:
                db.session.commit()
                db.session.add(approve_message)
                db.session.commit()
                flash("The application has been rejected and a message was sent to the user!", "success")
                return redirect(url_for(return_path, id=user_id))
            except:
                flash("There was a problem rejecting this application. Please try again later", "danger")
                return redirect(url_for(return_path, id=user_id))

            flash("The request.get('approve') was not = to 'True'", "danger")
            return redirect(url_for('manage.manage_index'))
    return redirect(url_for('main.index'))

@manage.route('/applications/<status>', methods=['GET'])
@login_required
def manage_applications_status(status):
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if status == "pending":
        applications = Application.query.filter(Application.status == "Application recieved").order_by(Application.app_date.desc()).all()
        notes = Notes.query.order_by(Notes.date_posted.desc()).all()
        return render_template('manage_applications.html', applications=applications, notes=notes, title=status)
    elif status == "approved":
        applications = Application.query.filter(Application.status == "Approved").filter(Application.user_id != None).order_by(Application.app_date.desc()).all()
        notes = Notes.query.order_by(Notes.date_posted.desc()).all()
        return render_template('manage_applications.html', applications=applications, notes=notes, title=status)
    elif status == "rejected":
        applications = Application.query.filter(Application.status == "Rejected").filter(Application.user_id != None).order_by(Application.app_date.desc()).all()
        return render_template('manage_applications.html', applications=applications, title=status)
    elif status == "deleted":
        applications = Application.query.filter(Application.user_id == None).order_by(Application.app_date.desc()).all()
        return render_template('manage_applications.html', applications=applications, title=status)
    else:
        return redirect(url_for('manage.admin'))


rank_list = ["Blank", "Web-Admin", "GM", "Assistant-GM", "Recruitment-Officer", "Officer", "Member", "Initiate", "Applicant", "Registered", "Rejected"]


@manage.route('/edit_users', methods=['POST'])
@login_required
def edit_users():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        database = db_name_to_object[request.form['db']]
        user_to_update = database.query.get_or_404(request.form['id'])
        user_to_update.username = request.form['username']
        user_to_update.rank = (rank_list.index(request.form['rank']))
        return_path = request.form['return']
        user_id = request.form['id']
        try:
            db.session.commit()
            flash("The User was successfully updated!", 'success')
            return redirect(url_for(return_path, id=user_id))
        except:
            flash("I was not able to update that user!", 'danger')
            return redirect(url_for(return_path, id=user_id))

    else:
        return redirect(url_for('main.index'))

@manage.route('/users/<status>', methods=['GET'])
@login_required
def manage_users(status):
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if status == "applicant":
        applications = Application.query.filter(Application.status == "Application recieved").order_by(Application.app_date.desc()).all()
        notes = Notes.query.order_by(Notes.date_posted.desc()).all()
        return render_template('manage_users.html', applications=applications, notes=notes, title=status)
    elif status == "member":
        applications = Application.query.filter(Application.status == "Approved").filter(Application.user_id != None).order_by(Application.app_date.desc()).all()
        notes = Notes.query.order_by(Notes.date_posted.desc()).all()
        users = User.query.options(load_only("id", "rank")).all()
        return render_template('manage_users.html', applications=applications, notes=notes, users=users, rank_list=rank_list, title=status)
    elif status == "rejected":
        applications = Application.query.filter(Application.status == "Rejected").filter(Application.user_id != None).order_by(Application.app_date.desc()).all()
        return render_template('manage_users.html', applications=applications, title=status)
    elif status == "deleted":
        applications = Application.query.filter(Application.user_id == None).order_by(Application.app_date.desc()).all()
        return render_template('manage_users.html', applications=applications, title=status)
    else:
        return redirect(url_for('manage.admin'))

@manage.route('/user/<id>')
@login_required
def user_control(id):
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(id)
    return render_template('user_control.html', user=user, rank_list=rank_list)


@manage.route('/search', methods=['POST'])
@login_required
def search():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    search = request.form['search']
    database = db_name_to_object[request.form['db']]
    results = database.query.filter(or_(database.title.like('%' + search + '%'), database.description.like('%' + search + '%'))).order_by(database.date.desc())
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
            flash("The Announcement was successfully updated!", 'success')
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
            flash("The Event was successfully updated!", 'success')
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
        devotional_to_update.date_updated = datetime.now()
        devotional_to_update.lead = request.form['lead']

        try:
            db.session.commit()
            flash("The Devotional was successfully updated!", 'success')
            return redirect('/devotionals')
        except:
            return "There was an issue updating this record. Please go back!"

    elif request.form['db'] == 'News_cast':
        news_cast_to_update = News_cast.query.get_or_404(request.form['id'])
        # news_cast_to_update.title = request.form['title']
        date = request.form['date']
        split_date = date.split('-')
        news_cast_to_update.title = 'News Cast for ' + split_date[1] + "-" + split_date[2] + "-" + split_date[0]
        news_cast_to_update.date = date
        news_cast_to_update.embed = request.form['embed']
        news_cast_to_update.description = request.form['description']
     

        try:
            db.session.commit()
            flash("The News Cast was successfully updated!", 'success')
            return redirect('/news-casts')
        except:
            return "There was an issue updating this record. Please go back!"

    return redirect('/admin')

# Generic POST route to insert data to the db
# You must pass the "db" in on the form and then create the object from the form data
# Last try to insert this object into the db
@manage.route('/insert', methods=['POST'])
@login_required
def insert():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    if request.form['db'] == 'Announcement':
        title = request.form['title']
        description = request.form['description']
        link = request.form['link']
        new_announcement = Announcement(title=title, description=description, link=link)        
        try:
            db.session.add(new_announcement)
            db.session.commit()
            flash("The Announcement was successfully added!", 'success')
            return redirect('/announcements')
        except:
            return "There was an issue updating this announcement :("

    elif request.form['db'] == 'Calendar':
        title = request.form['title']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        time = request.form['time']
        description = request.form['description']
        try:
            symbol = name_to_symbol[request.form['symbol']]
        except:
            symbol = "/static/main/img/other-icon.png"
        lead = request.form['lead']
        if int(request.form['n-times']) == 0:
            new_event = Calendar(title=title, date=date, time=time, description=description, symbol=symbol, lead=lead)
            try:
                db.session.add(new_event)
                db.session.commit()
                flash("The Event was successfully added!", 'success')
                return redirect('/events')
            except:
                return "There was an issue adding this event. Please go back!"
        else:
            repeat_num_days = int(request.form['n-days'])
            repeat_num_times = int(request.form['n-times'])
            repeat_delta = timedelta(days=repeat_num_days)
            for _ in range(repeat_num_times):
                new_event = Calendar(title=title, date=date, time=time, description=description, symbol=symbol, lead=lead)
                try:
                    db.session.add(new_event)
                    db.session.commit()
                except:
                    return "There was a problem adding this to the database :("
                date += repeat_delta
            flash("All events were successfully added!", 'success')
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
            flash("The Devotional was successfully added!", 'success')
            return redirect('/devotionals')
        except:
            return "There was an issue adding this devotional. Please go back!"

    elif request.form['db'] == 'News_cast':
        date = request.form['date']
        split_date = date.split('-')
        title = 'News Cast for ' + split_date[1] + "-" + split_date[2] + "-" + split_date[0]
        embed = request.form['embed']
        description = request.form['description']
        new_news_cast = News_cast(title=title, date=date, embed=embed, description=description)
        try:
            db.session.add(new_news_cast)
            db.session.commit()
            flash("The News Cast was successfully added!", 'success')
            return redirect('/news-casts')
        except:
            return "There was an issue adding this news cast. Please go back!"

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
        flash("All search results were successfully deleted!", 'success')
        return redirect('/events')
    
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
    elif request.form['db'] == 'News_cast':
        news_cast_to_delete = News_cast.query.get_or_404(request.form['id'])
        try:
            db.session.delete(news_cast_to_delete)
            db.session.commit()
            flash("News Cast was deleted successfully!", "success")
            return redirect('/news-casts')
        except:
            return "There was a problem deleting this news cast. Please go back!"
    elif request.form['db'] == 'User':
        user_to_delete = User.query.get_or_404(request.form['id'])
        try:            
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User was deleted successfully!", "success")
            return redirect(url_for('main.index'))
        except:
            flash("There was a problem deleting this account. Please try again later or send an email to drewxcom@gmail.com for support.", "danger")
            return "There was a problem deleting this User. Please go back!"

    return redirect('/admin')

@manage.route('/notes', methods=['POST'])
@login_required
def notes():
    if current_user.rank > 5:
        flash("You do not have a high enough rank to access this page!", 'danger')
        return redirect(url_for('main.index'))
    req = request.form
    from_user = current_user.username
    from_user_image = current_user.image_file
    note_type = req.get('type')
    user_id = req.get('user_id')
    note_text = req.get('note')
    return_path = req.get('return')

    if req.get('return'):
        return_path = req.get('return')
    else:
        return_path = "main.account"

    note = Notes(from_user=from_user, from_user_image=from_user_image, note_type=note_type, user_id=user_id, note=note_text)

    try:
        db.session.add(note)
        db.session.commit()
    except:
        flash("There was an issue posting this note. My bad :( Please try again later", "danger")
        return redirect(url_for(return_path, id=user_id))
    flash("Note was added successfully!", "success")
    return redirect(url_for(return_path, id=user_id))


@manage.route('/changelog')
def change_log():
    return render_template('change_log.html')