from flask import render_template, url_for, request, redirect, flash
from flask_app import app, db, bcrypt
from flask_app.models import Devotional, User
from forms import RegistrationForm, LoginForm
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created and you are now able to login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'd@mail.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/devotional')
def devotionals():
    devotionals = Devotional.query.order_by(Devotional.date.desc()).all()

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