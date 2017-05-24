from flask import Flask, flash, request, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from wtforms import StringField, FloatField, DateField, FileField, SubmitField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
basedir = os.path.dirname(os.path.realpath('__file__'))
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


manager = Manager(app) 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



UPLOAD_FOLDER = os.path.dirname(os.path.realpath('__file__')) + '/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav'])

# Go Away


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['DEBUG'] = True








class Artwork(db.Model):
	__tablename__ = 'artwork'
	id = db.Column(db.Integer, primary_key=True)
	artist = db.Column(db.Text())
	title = db.Column(db.Text(), unique=True, index=True)
	mediums = db.Column(db.Text())
	width = db.Column(db.Float())
	height = db.Column(db.Float())
	depth = db.Column(db.Float())
	date = db.Column(db.DateTime(), default=datetime.utcnow())
	location = db.Column(db.Text())
	description = db.Column(db.Text())
	notes  = db.Column(db.Text())
	art_upload_url = db.Column(db.Text())
	art_upload_type = db.Column(db.Text())


# implement Artist class which has relationship to artwork

class ArtworkForm(FlaskForm):
	artist = StringField("Artist's Name: ", validators=[DataRequired()])
	title = StringField("Work Title: ", validators=[DataRequired()])
	mediums = StringField("Work Medium/s: ", validators=[DataRequired()])
	width = FloatField("Width: ", validators=[DataRequired()])
	height = FloatField("Height: ", validators=[DataRequired()])
	depth = FloatField("Depth: ", validators=[DataRequired()])
	date = DateField("Date: ", validators=[DataRequired()])
	location = StringField("Artist's Name: ", validators=[DataRequired()])
	description = StringField("Artist's Name: ", validators=[DataRequired()])
	notes  = StringField("Artist's Name: ", validators=[DataRequired()])
	art_file = FileField("Image Upload")
	art_upload_type = StringField("FileType ", validators=[DataRequired()])
	submit = SubmitField('Submit')


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET','POST'])
def index():
	form = ArtworkForm()
	if request.method == 'POST':
		# title = Artwork.query.filter_by(title=form.title.data).first()
		# if title is None:
		artwork = Artwork(	artist=form.artist.data,
							title=form.title.data,
							mediums=form.mediums.data,
							width=form.width.data,
							height=form.height.data,
							depth=form.depth.data,
							date=form.date.data,
							location=form.location.data,
							description=form.description.data,
							notes=form.notes.data,
							# art_upload_url=form.artfile.__name__ #I havent the slightest
							art_upload_type=form.art_upload_type.data
							)
		db.session.add(artwork)
		db.session.commit()
		flash('Shoulda committed')
		return redirect(url_for('crap'))
	template = '''<form action="/crap" method="post">
				{0}<br>
				{1}<br>
				{2}<br>
				{3}<br>
				{4}<br>
				{5}<br>
				{6}<br>
				{7}<br>
				{8}<br>
				{9}<br>
				{10}<br>
				{11}<br>
				</form>
				'''.format(
					form.artist,
					form.title,
					form.mediums,
					form.width,
					form.height,
					form.depth,
					form.date,
					form.location,
					form.description,
					form.notes,
					form.art_upload_type,
					form.submit)
	return template

@app.route('/crap', methods=['GET','POST'])
def crap():
	artwork = Artwork()
	artworks = artwork.query.all()
	return '{0}'.format(artworks)




if __name__ == "__main__":
	db.create_all()
	manager.run()