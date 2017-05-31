import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

class Shortly(object):
	def __init__(self, config):
		self.redis = redis.Redis(config['redis_host'], config['redis_port'])
	def dispatch_request(self,request):
		return Response('Hello World!')
	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)