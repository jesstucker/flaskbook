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
    request.get_data(as_text=True)
    if os.path.exists('database.txt'):
    	database = open('database.txt', 'a')
    else:	
    	database = open('database.txt', 'w')
    database.write(request.form['say'] + ',' + request.form['to'] + '\n')
    database = open('database.txt', 'r')
    return \
    '''
      <p>
	      Say: {0} <br> 
	      To: {1} <br>
	      Form Data Unparsed:{2} <br>
	      Stored: <br> {3} <br>
      </p>
	'''.format(\
		request.form['say'],\
		request.form['to'], \
		request.data,\
		database.read().replace('\n', '<br>')
		)


if __name__ == "__main__":
    app.run()