# https://youtu.be/Z1RJmh_OqeA?t=1481

from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default= datetime.utcnow)

#     def __repr__(self):
#         return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting the task :('

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form['content']
#         print('This is the request.form - content ', request.form)
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'Couldn\'t update this record'
#     else:
#         return render_template('update.html', task=task)


@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)