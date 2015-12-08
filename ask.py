""" The back-end of Ask. """


from werkzeug.wrappers import Request, Response
import logging
import requests

import fixes

from reply import get_reply


# Set up output file for logs
logging.basicConfig(filename='/Apps/MAMP/logs/request.log', level=logging.INFO)
# Make requests output only warnings or errors
logging.getLogger('requests').setLevel(logging.WARNING)






def application(environ, start_response):
	""" Main WSGI callable function.

	This function is called when the server receives a request.
	It expects the request to contain the "text"
	parameter, and an optional "phone" parameter. Calls get_reply
	and dispatches a reply SMS to the SMSGateway app server
	(via send_sms). Returns a Werkzeug Response containing the phone
	and reply."""

	request = Request(environ)
	http_method = request.method
	
	# Our server receives an SMS using a GET Request.
	# I'd use POST if it was my choice, but the
	# creator of SMS Gateway chose GET :(.
	if http_method == 'GET':
		params = request.args
		
		phone = params.get('phone')
		user_message = params.get('text')
		# Workaround until we figure out Unicode:
		phone = fixes.asciified(phone)
		user_message = fixes.asciified(user_message)

		log("Received", phone, user_message, begin=True)
		

		reply_message = get_reply(user_message, phone)
		log("Sent", phone, reply_message, end=True)
		
		if __name__ != '__main__':
			send_sms(phone, reply_message)
		
	#response = Response('', mimetype='text/html')
	response = Response(reply_message, mimetype='text/html')
	return response(environ, start_response)






def send_sms(phone, message, url='http://192.168.1.101:6969/sendsms'):
	"""Sends an HTTP GET request containing the SMS.

	The request contains:
	- 'phone'
	- 'message'
	Which is the format expected by SMS Gateway."""
	
	# sms_gateway_url = url
	# sms_gateway_url = 'http://192.168.43.78:6969/sendsms'
	sms_gateway_url = 'http://192.168.43.94:6969/sendsms'
	message_params = {'phone': phone, 'text': message}
	
	# Again - not my idea, just what SMSG requires :(
	requests.get(sms_gateway_url, params=message_params)



# might make it more versatile in the future
def log(event, phone, message, begin=False, end=False, line_len=20):
	""" Logs the number and message. Optional args begin and end
	add some separators and spacing."""

	phone = fixes.asciified(phone)
	message = fixes.asciified(message)

	word_len = len(event) + 2 #for two spaces
	left = (line_len - word_len) // 2
	right = line_len - (left + word_len)
	
	
	if begin: logging.info(' ' + '*'*line_len)
	
	logging.info(" {L} {ev} {R} ".format( L=left*'-', ev=event, R=right*'-' ))
	logging.info(" " + phone)
	logging.info(" " + message)
	
	if end: logging.info('\n\n')






if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	server = make_server('localhost', 80, application)

	print(
		"Server running on http://localhost.\n"
		"To test, go to http://localhost/ask?text=app%20params\n"
		"To close the server, press Ctrl + C.\n"
	)
	server.serve_forever()