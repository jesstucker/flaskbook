import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask import make_response
from flask import redirect
from flask import abort
#fom flask.ext.script import Manager
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from threading import Thread

# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(os.path.realpath('__file__'))
app = Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'stmp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
            sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


manager = Manager(app) 
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Role %r>' % self.name

    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r' % self.username

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET','POST'])
def index():
    # makes an instance of the form
    form = NameForm()
    # validates form input, i guess for security reasons. not sure
    if form.validate_on_submit():
        # tricky coupling here. kind of annoying for a beginner actually
        # checks database to see whether there's already an instance of
        # the name entered in the form. 
        user = User.query.filter_by(username=form.name.data).first()
        # if there is no instance, it enters it into the database, like so:
        if user is None:
            # takes user variable and makes new User class instance of it
            # by taking property 'username' and inserting it to the User model
            user = User(username = form.name.data)
            # then adds it to the session. I do not understand sessions.
            # get a concise definition of it then[y]
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                        'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
            form = form, name = session.get('name'),
            known = session.get('known', False))

# Nice to have webpages about error handling
#but of not great concern during development.
#before you take exception, just no
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Nice to have webpages about error handling
#but of not great concern during development.
#before you take exception, just no
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.hmtl'), 500


#@app.route('/user/<id>')
#def get_user(id):
#    user = load_user(id)
#    if not user:
#        abort(404)
#    return '<h1>Hello, %s</h1>' % user.name

#Not great concern but great simple example!
@app.route('/redirect')
def redir():
    return redirect('http://www.example.com')

#Not great concern but great simple example!
@app.route('/bad')
def bad():
    return '<h1>Bad request, man</h1>', 400

#Not great concern but great simple example!
@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

#Not great concern but great simple example!
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    db.create_all()
    manager.run(debug=True)