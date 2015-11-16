""" Launcher app for Ask """

from werkzeug.wrappers import Request, Response
from werkzeug.datastructures import ImmutableOrderedMultiDict
from json import dumps
import logging

logging.basicConfig(filename='/Apps/MAMP/logs/request.log', level=logging.INFO)


def application(environ, start_response):
	request = Request(environ)
	request.parameter_storage_class = ImmutableOrderedMultiDict
	
	
	method = request.method
	
	result = ''
	
	if method == 'GET':
		params = request.args
		logging.info(params)
		logging.info('*******************\n')
			
	if method == 'POST':
	
		data = request.form
		logging.info(data)
		logging.info('*******************\n')
		
		number = "+48572035498"
		# result = dumps(response_dict)
		
		

	response = Response(result, mimetype='application/json')
	return response(environ, start_response)
	
if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	server = make_server('localhost', 80, application)
	server.serve_forever()