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
import httplib, urllib
from optparse import OptionParser

USER_ID="YOUR ID HERE"
API_TOKEN="API_TOKEN"

def send_message(message):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
		"token": API_TOKEN,
		"user": USER_ID,
		"message": message,
	}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	
	
def send_silent(message):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
		"token": API_TOKEN,
		"user": USER_ID,
		"message": message,
		"sound":"none",	
	}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()
	
	
parser = OptionParser()
parser.add_option("-m", "--message", dest="message",
				help="set message for notification", metavar="MESSAGE")
parser.add_option("-s", "--silent",
				action='store_true', dest="silent", default = False,
				help="silent notification")
(options, args) = parser.parse_args()
if options.silent:
	send_silent(options.message)
else:
	send_message(options.message)
				  
