import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask import make_response
from flask import redirect
from flask import abort
#from flask.ext.script import Manager
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

basedir = os.path.abspath(os.path.dirname(__file__))

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
app.config('MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')



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
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
            form = form, name = session.get('name'),
            known = session.get('known', False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.hmtl'), 500


#@app.route('/user/<id>')
#def get_user(id):
#    user = load_user(id)
#    if not user:
#        abort(404)
#    return '<h1>Hello, %s</h1>' % user.name

@app.route('/redirect')
def redir():
    return redirect('http://www.example.com')

@app.route('/bad')
def bad():
    return '<h1>Bad request, man</h1>', 400

@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    db.create_all()
    manager.run()

