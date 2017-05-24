import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'art.sqlite3')
app.config['SECRET_KEY'] = 'RANDOM STRING'

db = SQLAlchemy(app)

class Artwork(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    mediums = db.Column(db.String(500))
    description = db.Column(db.String(500))

    def __init__(self, title, mediums, description):
        self.title = title
        self.mediums = mediums
        self.description = description

#@app.route('/')
#def show_all():
#    return render_template('show_all.html', artwork=Artwork.query.all())

@app.route('/', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Please enter title, at least, geesh', 'error')
        else:
            artwork = Artwork(  request.form['title'],
                                request.form['mediums'],
                                request.form['description'])
            db.session.add(artwork)
            db.session.commit()

            flash('Artwork was successfully added')
            return redirect(url_for('new'))
    return render_template('new.html', artwork=Artwork.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
