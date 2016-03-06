import webapp2
import json
import ast
import models
import jinja2
import os
import uuid
import datetime
from models import ResultSet
from models import Result
from models import Pi

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
	# Used for home page
    def get(self):
    	template_values = {'num_sets': models.get_num_unique_sets(),
    						'unique_results': models.get_unique_results(),
    						'last_result': models.get_last_submission()}

    	template = JINJA_ENVIRONMENT.get_template('index.html')

        self.response.write(template.render(template_values))

class DataHandler(webapp2.RequestHandler):
	#  send-data route is used by Rasberry Pi Client devices to send MAC collections
	def post(self):
		jsonobject = json.loads(self.request.body)
		auth = jsonobject['auth']
		results = jsonobject['results']
		time = datetime.datetime.strptime(jsonobject['time'], "%Y-%m-%d %H:%M:%S")

		if models.device_registered(auth):
			if results:
				result_set = ResultSet()
				result_set.standard_time = roundTime(time,roundTo=5*60)
				result_set_key = result_set.put()

				for key, value in results.iteritems():
					db_result = Result(mac_address=key, signal=value, result_set=result_set_key)
					db_result.put()

			self.response.write('Should have put items in data store')
		else:
			self.response.write('Device not registered')

class RegisterHandler(webapp2.RequestHandler):
	# Used to check to see if a device is currently registered. URL parameter token used
	def get(self):
		token = self.request.get('token')
		self.response.write(models.device_registered(token))

	# Used for a device to be registered. Device submits unique token and name the device wants to be
	def post(self):
		jsonobject = json.loads(self.request.body)
		token = jsonobject['token']
		name = jsonobject['name']

		dev_reg = models.device_registered(token)

		if (dev_reg==True):
			self.response.write('Device already registered')
		elif (dev_reg==False):
			models.register_pi(token, name)
			self.response.write('Registered device')
		else:
			self.response.write('Incorrect Device ID')

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/send-data', DataHandler),
    ('/register', RegisterHandler),
], debug=True)