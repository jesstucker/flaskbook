from flask import Flask, request
app = Flask(__name__)



import pprint
class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(environ, log_response)


@app.route('/', methods=['GET'])
def index():
	return '''
	<form action='/results' method='post'>
	<input type='text' name='fname'><br>
	<input type='submit'>
	</form>
	'''


@app.route('/results', methods=['POST'])
def results():
	return '''
	<H1>RESULTS:</H1>{}
	<H1>REQUESTD DETAILS:
	'''.format((str(request.__dict__)).replace(',', '<br>'))

if __name__ == "__main__":
	app.wsgi_app = LoggingMiddleware(app.wsgi_app)
	app.run(debug=True)