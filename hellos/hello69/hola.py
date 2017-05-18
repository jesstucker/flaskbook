from flask import Flask, request
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return '''
		<form method="post" action="/hello">
		  <label for="say">SAY WHAT?</label><input name="say">
		  <label for="to">TO WHOM?</label><input name="to">
		  <button>Send POST</button>
		</form>
		'''

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    request.get_data()
    if os.path.exists('database.txt'):
    	database = open('database.txt', 'a')
    else:	
    	database = open('database.txt', 'w')
    database.write(request.form['say'] + ',' + request.form['to'] + '\n')
    database = open('database.txt', 'r')
    return \
    '''<p>Say: {0} <br>'''.format(request.form['say']) + \
	'''   To: {0} <br>'''.format(request.form['to']) + \
	'''   Form Data Unparsed:{0} <br>'''.format(request.data) + \
	'''   Stored: <br> {0} <br>'''.format(database.read()) + \
    '''</p>'''

if __name__ == "__main__":
    app.run(debug=True)