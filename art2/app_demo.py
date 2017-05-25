import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['UPLOAD_FOLDER'] = basedir


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
        file = request.files['upload']
        filename = file.filename
        file.save(filename)

        artwork = Artwork(  request.form['title'],
                            request.form['mediums'],
                            request.form['description'],
                            str(filename)
                                )
        db.session.add(artwork)
        db.session.commit()
        return redirect(url_for('new'))
    return render_template('new_demo.html', artwork=Artwork.query.all())

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)