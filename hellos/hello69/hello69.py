import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask import make_response
from flask import redirect
from flask import abort

from flask_script import Manager
from flask import render_template

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, Text=Text)
manager.add_command("shell", Shell(make_context=make_shell_context))



class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Text %r' % self.text


class TextForm(FlaskForm):
    name = StringField('What is your text?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET','POST'])
def index():
    form = TextForm()
    if form.validate_on_submit():
        text = Text.query.filter_by(text=form.name.data).first()
        if text is None:
            text = Text(text = form.name.data)
            db.session.add(text)
            session['known'] = False

        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
            form = form, name = session.get('name'),
            known = session.get('known', False))


if __name__ == '__main__':
    db.create_all()
    manager.run()
