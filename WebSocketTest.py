import Leap
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.websocket import WebSocketHandler
import random

#This is intended to faciliate communication between Leap Motion and ROS
#The current data is only a placeholder
#It will be replaced by actual processed tracking info once implemented

class LeapWSHandler(WebSocketHandler):
	clients = [] #list of listening clients

	def check_origin(self, origin):
		return True

	def test(self):
		return self.send_data("x: " + str(random.random()*2))

	def open(self):
		LeapWSHandler.clients.append(self)
		self.callback = PeriodicCallback(self.test, 1000)
		self.callback.start()

	def on_message(self, message):
		print message

	def on_close(self):
		LeapWSHandler.clients.remove(self)
		self.callback.stop()

	@classmethod
	def send_data(l, data):
		for client in l.clients:
			try:
				client.write_message(data)
			except:
				print "Fail to send data to client."

def main():
	#tornado.ioloop.IOLoop.instance().stop()
	app = Application([
		(r"/ws", LeapWSHandler),
	])

	hs = HTTPServer(app)
	hs.listen(8888)
	IOLoop.instance().start()

main()
