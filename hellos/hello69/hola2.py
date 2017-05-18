from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return '''
		<form method="post" action="/post">
		  <label for="say">SAY WHAT?</label><input name="say">
		  <label for="to">TO WHOM?</label><input name="to">
		  <button>Send POST</button>
		</form>
		'''

@app.route('/post', methods=['GET', 'POST'])
def hello():
	database = open('database.txt', 'wb')
    database.write(request.form['say'] + ',' + request.form['to'] + '\n')
    database.seek(0)
    return 'Stored: <br> {0} <br>'.format(database.read().replace('\n', '<b>')) + \

if __name__ == "__main__":
    app.run(debug=True)