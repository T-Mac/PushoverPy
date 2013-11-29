#!/usr/bin/python
"""
	Copyright 2013 Taylor McKinnon
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from optparse import OptionParser
import requests
				  
class Pipeline(object):
	filters = []
	def Register(self, filter):
		self.filters.append(filter)
		
	def Execute(self, msg):
		for filter in self.filters:
			r = filter.Execute(msg)
			msg = r
		return msg
		
class Pushover(object):
	def __init__(self, user_key, api_token):
		self.pipeline = Pipeline()
		self.pipeline.Register(Payload_Filter(user_key, api_token))
		self.pipeline.Register(Api_Filter())
		self.pipeline.Register(Response_Filter())
		
	def send(self, message, priority = 0, kwargs=None):
		msg = Message(message, priority, kwargs)
		msg = self.pipeline.Execute(msg)
		return msg
		
		
class Message(object):
	def __init__(self, message, priority = 0, kwargs=None):
		self.message = message
		self.options = kwargs
		self.priority = priority
		
class Payload_Filter(object):
	def __init__(self, user_key, api_token):
		self.user_key = user_key
		self.api_token = api_token
		
	def Execute(self, msg):
		payload = {
			'token':self.api_token,
			'user':self.user_key,
			'message':msg.message,
			'priority':msg.priority
			}
		#print payload
		if msg.options:
			payload.update(msg.options)
		msg.payload = payload
		#print payload
		return msg
		
class Api_Filter(object):
	def Execute(self, msg):
		response = requests.post('https://api.pushover.net/1/messages.json', params = msg.payload)
		msg.response = response
		return msg
		
class Response_Filter(object):
	def Execute(self, msg):
		if msg.response.json()['status'] == 1:
			msg.success = True
		else:
			msg.success = False
			msg.error = msg.response.json()['errors']
		return msg
		
if __name__ == '__main__':	
	parser = OptionParser()
	parser.add_option("-m", "--message", dest="message",
					help="set message for notification", metavar="MESSAGE")
	parser.add_option("-s", "--silent",
					action='store_true', dest="silent", default = False,
					help="silent notification")
	parser.add_option("-t", "--token", dest="token",
					help="Api Token")
	parser.add_option("-u", "--user-key", dest="user",
					help="User Key")
	parser.add_option("-p", "--priority", 
					type='int', dest="priority", default = 0,
					help="Set Message to Priority")
					
	(options, args) = parser.parse_args()
	Api = Pushover(options.user, options.token)
	if options.silent:
		r = Api.send(options.message, -1)
	else:
		r = Api.send(options.message, options.priority)
	
	if r.response.json()['status'] == 1:
		print 'Success'
	else:
		print r.response.text