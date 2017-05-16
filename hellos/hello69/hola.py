from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return '''
		<form method="post" action="/hello">

		  <label for="say">SAY WHAT?</label>
		  <input name="say">

		  <label for="to">TO WHOM?</label>
		  <input name="to">

		  <button>Send POST</button>

		</form>
		'''

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return \
    '''
      <p>
	      Say: {0} <br> 
	      To: {1} <br>
	      Python Values:{2} <br>
	      Browser Submitted Values: {3} <br>
	      Stream attempt: {4}
      </p>
	'''.format(\
		request.form['say'],\
		request.form['to'], \
		request.values, \
		request.get_data(as_text=True),\
		request.stream.read(),\
		)


if __name__ == "__main__":
    app.run()