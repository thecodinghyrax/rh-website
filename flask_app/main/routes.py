from flask import Blueprint, request, send_from_directory, render_template, redirect, url_for, flash
from flask_app import app, db, bcrypt, ext, mail
from flask_app.models import Devotional, News, Calendar, User, Announcement, Application, UserMessages
import os
import calendar
from datetime import date, datetime, timedelta
from sqlalchemy import extract, and_, or_
from flask_login import current_user, login_user, logout_user, login_required
from flask_app.main.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, ApplyToGuildForm
from flask_mail import Message
import secrets
from PIL import Image


main = Blueprint('main', __name__,
                template_folder='templates')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='noreply@renewedhope.us', 
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}
Please note: This token will expire in 30 minutes from the time this email is sent. 

If you did not make this request, please ignore this email. No chnages will be made.
'''
    mail.send(msg)

def send_applied_email():
    mail_to_user_list = User.query.filter(User.rank <= 5).all()
    mail_to_email_list = []
    for user in mail_to_user_list:
        mail_to_email_list.append(user.email)
    msg = Message('We have a new applicant', 
                    sender='noreply@renewedhope.us', 
                    recipients=mail_to_email_list)
    msg.body = f'''Someone just applied to join. Please login to the admin panel of the website to approve, reject or just message the appliciant. 
{url_for('manage.manage_applications', _external=True)}

'''
    mail.send(msg)

# @main.route('/testpage')
# def testpage():
#     pic_route = url_for('static', filename='main/img/profile_pics/')
#     applications = Application.query.filter(Application.status >= 'A').filter(Application.name >= "J").all()
#     users = User.query.all()
#     messages = UserMessages.query.all()
#     return render_template('testpage.html', applications=applications, users=users, messages=messages, pic_route=pic_route)


@main.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@main.route('/')
def index():
    devotional = Devotional.query.order_by(Devotional.date.desc()).first()
    news = News.query.order_by(News.id.asc()).all()
    announcements = Announcement.query.order_by(Announcement.id.desc()).all()
    if current_user.is_authenticated:
        user_msgs = User.query.filter(User.id == current_user.id).all()
        has_read = 0
        for msg in user_msgs[0].messages:
            if msg.has_read != True:
                has_read =+ 1
    else:
        has_read = 0
    if current_user.is_authenticated and current_user.rank < 6:
        no_ack_query = db.session.query(UserMessages.acknowledged).filter(UserMessages.acknowledged == False).all()
        no_ack = len(no_ack_query)
    else:
        no_ack = 0

    return render_template('index.html', current_user=current_user, devotional=devotional, news=news, announcements=announcements, no_ack=no_ack, has_read=has_read, title="Renewed Hope Guild Home Page")


@ext.register_generator
def index():
    yield 'main.index', {}


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@main.route('/guild_calendar')
def guild_calendar():
    today = datetime.now() - timedelta(hours=6)
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
 
    events = Calendar.query.filter(extract('month', Calendar.date) == month, extract('year', Calendar.date) == year).all()
    current_day = today.day
    month_name = calendar.month_name[month]
    cal = calendar.Calendar()
    cal.setfirstweekday(calendar.SUNDAY)
    current_cal = cal.monthdayscalendar(year, month)
    if len(current_cal) < 6:
        extra_week = [[0,0,0,0,0,0,0]]
        current_cal += extra_week

    return render_template('calendar.html', cal=current_cal, month=month, month_name=month_name, current_month=current_month, year=year, events=events, current_day=current_day, title="Renewed Hope Guild Calendar")

@ext.register_generator
def guild_calendar():
    yield 'main.guild_calendar', {}


@main.route('/discord')
def discord():
    return render_template('discord.html', title="Renewed Hope Guild Discord")


@ext.register_generator
def discord():
    yield 'main.discord', {}


@main.route('/devotional')
def devotionals():
    page = request.args.get('page', 1, type=int)
    devotionals = Devotional.query.order_by(Devotional.date.desc()).paginate(page=page, per_page=5)

    return render_template('devotional.html', devotionals=devotionals, title="Devotionals for the Renewed Hope Guild")


@ext.register_generator
def devotionals():
    yield 'main.devotionals', {}


@main.route('/about')
def about():
    return render_template('about.html', title="All About the Renewed Hope World of Warcraft Guild")


@ext.register_generator
def about():
    yield 'main.about', {}


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please verify email and password', 'danger')
    return render_template('login.html', title="Login", form=form)


def save_picture(form_picture, pic_to_delete):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/main/img/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    if pic_to_delete != None:
        picture_path_to_delete = os.path.join(app.root_path, 'static/main/img/profile_pics', pic_to_delete)
        os.remove(picture_path_to_delete)
    return picture_fn

rank_dict = {1:"Web-Admin", 2:"GM", 3:"Assistant-GM", 4:"Recruitment-Officer", 5:"Officer", 6:"Member", 7:"Member", 8:"Initiate", 9:"Applicant", 10:"Registered", 11:"Rejected"}

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    selected_pic = "This is the default statment"
    if form.validate_on_submit():

        if form.picture.data != current_user.image_file and form.picture.data != None:
            if current_user.image_file != 'default.jpg':
                pic_to_delete = current_user.image_file
            else:
                pic_to_delete = None

            selected_pic = form.picture.data
            picture_file = save_picture(form.picture.data, pic_to_delete)
            msg_to_update = UserMessages.query.filter(UserMessages.user_id == current_user.id).filter(UserMessages.from_user == current_user.username).all()
            try:
                for msg in msg_to_update:
                    msg.from_user_image = picture_file
                    db.session.commit()
                current_user.image_file = picture_file
                db.session.commit()
                flash('Your profile picture has been updated!', 'success')
            except:
                flash('There was a problem updating your old message profile pictures. Please try again later :(', 'danger')
                return redirect(url_for('main.account'))

        if form.username.data != current_user.username:
            msg_to_update = UserMessages.query.filter(UserMessages.user_id == current_user.id).filter(UserMessages.from_user == current_user.username).all()
            try:
                for msg in msg_to_update:
                    msg.from_user = form.username.data
                    db.session.commit()
                current_user.username = form.username.data
                db.session.commit()
                flash('Your username has been updated!', 'success')
            except:
                flash('There was a problem updating your old message user names. Please try again later :(', 'danger')
                return redirect(url_for('main.account'))

        if form.email.data != current_user.email:
            try:
                current_user.email = form.email.data
                db.session.commit()
                flash('Your email has been updated!', 'success')
                return redirect(url_for('main.account'))
            except:
                flash('There was a problem updating your picture. Please try again later :(', 'danger')
                return redirect(url_for('main.account'))
   
    unread_messages = UserMessages.query.filter_by(user_id = current_user.id).all()
    for message in unread_messages:
        message.has_read = True
        db.session.commit()
    msg_query = db.session.query(UserMessages.from_user, UserMessages.from_user_image, UserMessages.message_date,
                                UserMessages.message_body, UserMessages.user_id, User.username, User.id, User.image_file).join(UserMessages, UserMessages.user_id == User.id)
    messages = msg_query.filter(User.id == current_user.id).order_by(UserMessages.message_date).all()
    form.username.data = current_user.username
    form.email.data = current_user.email
    rank = rank_dict[current_user.rank]
    image_file = url_for('static', filename='main/img/profile_pics/' + current_user.image_file ) 
    return render_template('account.html', title="Your Renewed Hope Guild Account Page", image_file=image_file, form=form, rank=rank, messages=messages, selected_pic=selected_pic)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = ApplyToGuildForm()
    if form.validate_on_submit():
        name = form.name.data
        join_how = form.join_how.data
        find_how = form.find_how.data
        self_description = form.self_description.data
        if form.b_tag:
            b_tag = form.b_tag.data
        else:
            b_tag = None
        have_auth = form.have_auth.data
        play_when = form.play_when.data
        status = "Application recieved"
        application = Application(name=name, join_how=join_how, find_how=find_how, self_description=self_description, b_tag=b_tag, have_auth=have_auth, play_when=play_when, status=status)
        from_user = "Renewed Hope WebBot"
        from_user_image = '655c9f17511a4133.png'
        body = "Congratulations, Your application has been received! \n\nWe have lit the signal fires and our guild leadership should be notified very soon. Your application will be reviewed and one of our fine officers will reach out to you soon to set up a time to chat. We like to take a few minutes and talk to all applicants before sending out an invite. This will give us a chance to get to know you a bit better and also give you a chance to ask any questions you may still have about the guild. Thanks for showing your interest in joining Renewed Hope and we look forward to talking to you soon."
        applied_message = UserMessages(from_user=from_user, from_user_image=from_user_image, message_body=body)

        try:
            send_applied_email()
            user = User.query.get(current_user.id)
            applied_message.user_id = current_user.id
            user.rank = 9
            application.user_id = current_user.id
            db.session.add(applied_message)
            db.session.add(application)
            db.session.commit()
            flash('Your application has been recieved! Please check here offten for updates on the status of your request.', 'success')
            return redirect(url_for('main.account'))
        except:
            flash('There was a problem submitting your application. We\'re sorry about that. Feel free to mail drewxcom@gmail.com about what happened!', 'danger')
            return redirect(url_for('main.index'))
    else:
        return render_template('apply.html', title="Apply to join the Renewed Hope Guild", form=form)

@main.route('/messages', methods=['POST'])
@login_required
def messages():
    req = request.form
    user = User.query.get(current_user.id)
    from_user = user.username
    from_user_image = user.image_file
    message_date = datetime.utcnow()
    message_body = req.get('message_body')
    if req.get('id'):
        user_id = req.get('id')
    else:
        user_id = current_user.id 
    if req.get('return'):
        return_path = req.get('return')
    else:
        return_path = "main.account"
    if req.get('acknowledged'):
        acknowledged = False
    else:
        acknowledged = True
    message = UserMessages(from_user=from_user, from_user_image=from_user_image, message_date=message_date,  message_body=message_body, acknowledged=acknowledged)
    try:
        msg_to_update = UserMessages.query.filter(UserMessages.user_id == user_id).filter(UserMessages.acknowledged == False).all()
        for msg in msg_to_update:
            msg.acknowledged = True
            db.session.commit()
    except:
        flash("There was an issue acknowlaging the message. My bad :( Please try again later", "danger")
        return redirect(url_for(return_path))
    try:
        message.user_id = user_id 
        db.session.add(message)
        db.session.commit()
        flash("Your message was submitted", "success")
        return redirect(url_for(return_path))
    except:
        flash("There was an issue submitting your message. My bad :( Please try again later", "danger")
        return redirect(url_for(return_path))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            from_user = "Renewed Hope WebBot"
            from_user_image = '655c9f17511a4133.png'
            message_date = datetime.utcnow()
            message_body = 'You are now registered!\nWelcome to the home of the Renewed Hope guild. From here you can apply to join the guild, message our leadership (via the reply button), update your information or delete your account.'
            message = UserMessages(from_user=from_user, from_user_image=from_user_image, message_date=message_date, message_body=message_body)
            message.user_id = current_user.id
            db.session.add(message)
            db.session.commit()
            flash(f'Your account has been created and you are now logged in', 'success')    
            return redirect(url_for('main.account'))
        except:
            flash(f'There was a problem regiestering your account. Please try back later.', 'danger')    
            return redirect(url_for('main.index'))
    return render_template('register.html', form=form, title="Register for access to the Renewed Hope Guild Website")


@main.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        logout_user()
    form = RequestResetForm()
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password. Please allow up to 10 minutes to recieve the mail.', 'info')
            return redirect(url_for('main.login'))
        except:
            flash('There was a problem resetting you password. Are you sure the email you entered was valid?', 'danger')
            return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset your Renewed Hope Guild Password', form=form)
    


@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect({{ url_for('main.reset_request') }})
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset your Renewed Hope Guild Password', form=form)

