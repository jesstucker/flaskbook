#import the main app
from flask import Flask
app = Flask(__name__)


#import the 'manager' stuff for shell executions
from flask_script import Manager
from flask_script import Shell
manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, Text=Text)
manager.add_command("shell", Shell(make_context=make_shell_context))


#The big ugly heap of database config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.dirname(os.path.realpath('__file__'))
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
class Text(db.Model):
    __tablename__ = 'texts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)
    def __repr__(self):
        return '%r' % self.text



from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
class TextForm(FlaskForm):
    name = StringField('What is your text?')
    submit = SubmitField('Submit')



from flask import render_template, session, redirect, url_for
@app.route('/', methods=['GET','POST'])
def index():
    form = TextForm()
    texts = Text.query.all()
    if form.validate_on_submit():
        text = Text.query.filter_by(text=form.name.data).first()
        text = Text(text = form.name.data)
        db.session.add(text)
        return redirect(url_for('index'))
    else:
        # return render_template('index.html',
        #         texts = texts,
        #         form = form,
        #         name = session.get('name')
        #         )
        return """
        <div>
            TEXTS:<br>
            {0}
        </div>
        <form action="" method="post">
            {1}
            {2}
            {3}
        </form>
        <div>ELSE CLAUSE</div>
        """.format(texts, form.csrf_token, form.name ,form.submit)


if __name__ == '__main__':
    db.create_all()
    manager.run()

