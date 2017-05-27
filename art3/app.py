#should be reduced down further to for demo
import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = basedir + '/static/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'art.sqlite3')
app.config['SECRET_KEY'] = 'RANDOM STRING'


db = SQLAlchemy(app)

class Artwork(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

    def __init__(self, title, image_url):
        self.title = title
        self.image_url = image_url


@app.route('/', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        file = request.files['upload']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        artwork = Artwork(  request.form['title'],
                            str('/static/' + filename)
                                )
        db.session.add(artwork)
        db.session.commit()
        return redirect(url_for('new'))
    return render_template('new.html', artwork=Artwork.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
