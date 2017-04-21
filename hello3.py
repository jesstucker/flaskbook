from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort
#from flask.ext.script import Manager
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)


#@app.route('/user/<id>')
#def get_user(id):
#    user = load_user(id)
#    if not user:
#        abort(404)
#    return '<h1>Hello, %s</h1>' % user.name

@app.route('/redirect')
def redir():
    return redirect('http://www.example.com')

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

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
    return '<h1>Hello, %s!</h1>' % name

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    manager.run()
