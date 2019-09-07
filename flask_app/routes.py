from flask import render_template, url_for, request, redirect, flash, send_from_directory
from flask_app import app, db, bcrypt
from flask_app.models import Devotional, User
from forms import RegistrationForm, LoginForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user
import os

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def index():
    devotional = Devotional.query.order_by(Devotional.date.desc()).first()
    return render_template('index.html', devotional=devotional)

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.xml')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('add_devotional'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/devotional')
def devotionals():
    page = request.args.get('page', 1, type=int)
    devotionals = Devotional.query.order_by(Devotional.date.desc()).paginate(page=page, per_page=20)

    return render_template('devotional.html', devotionals=devotionals)

@app.route('/add_devotional', methods=['POST', 'GET'])
def add_devotional():
    if request.method == 'POST':
        date = request.form['date']
        discription = request.form['discription']
        link = request.form['link']
        title = request.form['title']
        date_updated = datetime.utcnow()
        new_devotional = Devotional(title=title, date=date, content=discription, download_link=link)
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

@app.route('/delete/<int:id>')
def delete(id):
    devotional_to_delete = Devotional.query.get_or_404(id)

    try:
        db.session.delete(devotional_to_delete)
        db.session.commit()
        return redirect('/add_devotional')
    except:
        return "There was an issue deleting the devotional :("

@app.route('/confirm/<int:id>')
def confirm(id):
    devotional = Devotional.query.get(id)
    return render_template('confirm.html', id=id, devotional=devotional)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    devotional_to_update = Devotional.query.get_or_404(id)
    if request.method == 'POST':
        devotional_to_update.title = request.form['title']
        devotional_to_update.date = request.form['date']
        devotional_to_update.content = request.form['discription']
        devotional_to_update.download_link = request.form['link']
        devotional_to_update.date_updated = datetime.utcnow()

        try:
            db.session.commit()
            return redirect('/add_devotional')
        except:
            return "There was an issue updating this devotional :("
    else:
        return render_template('update.html', devotional=devotional_to_update)

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
