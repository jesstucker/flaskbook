import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
static_dir = basedir + '/static/'

app.config['UPLOAD_FOLDER'] = static_dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'art.sqlite3')
app.config['SECRET_KEY'] = 'RANDOM STRING'


db = SQLAlchemy(app)

class Artwork(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    mediums = db.Column(db.String(500))
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))

    def __init__(self, title, mediums, description, image_url):
        self.title = title
        self.mediums = mediums
        self.description = description
        self.image_url = image_url


@app.route('/', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Please enter title, at least, geesh', 'error')
        else:
            file = request.files['upload']
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            artwork = Artwork(  request.form['title'],
                                request.form['mediums'],
                                request.form['description'],
                                str('static/' + filename)
                                )
            db.session.add(artwork)
            db.session.commit()

            flash('Artwork was successfully added')
            return redirect(url_for('new'))
    return render_template('new.html', artwork=Artwork.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
