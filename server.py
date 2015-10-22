""" Simple server for Text The Web """

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import parse_headers
import socketserver
from json import dumps

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		response_uni = "<html><body><h1>hi!</h1></body></html>"
		response = response_uni.encode('utf-8')
		self.wfile.write(response)

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
	
		length = int(self.headers.get_all("Content-Length")[0])
		posted_data_raw = self.rfile.read(length) #raw bytes
		posted_data = posted_data_raw.decode('utf-8')
		
		if self.path == '/test':
			print(posted_data)
			response_uni = "<html><body><h1>" + posted_data + "</h1></body></html>"


		elif self.path == '/sms':
			# turn urlencode into dict with:
			# from urllib.parse import parse_qs
			
			# maybe it can be done without extracting raw message content?
			# sth like self.headers.get_all() idk
			
			#also: check if these work:
			# if response.headers['Content-Length'] works.
			# self.getheader('Content-Length'))
			# self.getheaders('Content-Length')
			#
			# source --> http://goo.gl/RtVCYO
			response_dict = {
				"payload": {
					"success": "true",
					"task": "send",
					"messages": [
						{
							"to": "+48-601-527-314",
							"message": "halo halo",
							"uuid": "042b3515-ef6b-f424-c4qd"
						}
					]
				}
			}
			response_uni = dumps(response_dict)

		else:
			response_uni = "<html><body><h1>POST!</h1></body></html>"
			
		response = response_uni.encode('utf-8')
		
		self._set_headers()
		self.wfile.write(response)
		
def run(server_class=HTTPServer, handler_class=S, port=8000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('Server running on port {}.'.format(port))
	httpd.serve_forever()


if __name__ == "__main__":
	run()

