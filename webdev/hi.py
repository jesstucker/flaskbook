import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand





app = Flask(__name__)
manager = Manager(app)


app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'POOP'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username



class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():
	user_agent = request.headers.items()
	form = NameForm()
	request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'
	result = request.data
	if request.method == "POST":
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

	return render_template('index.html', crap=user_agent, form=form, 
							result=result, name=session.get('name'),
							known = session.get('known', False))

@app.route('/user/<name>')
def user(name):
	
	return render_template('user.html', name=name)

if __name__ == '__main__':
	manager.run()

