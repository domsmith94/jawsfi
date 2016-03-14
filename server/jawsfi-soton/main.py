import webapp2
import json
import models
import jinja2
import os
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

        print('Recieved a request on send-data')

        if models.device_registered(auth):
            if results:
                models.process_results(results, time, auth)
                self.response.write('Should have put items in data store')
        else:
            self.response.set_status(401)
            self.response.write('Device not registered')


class RegisterHandler(webapp2.RequestHandler):
    # Used to check to see if a device is currently registered. URL parameter token used
    def get(self):
        token = self.request.get('token')
        self.response.write(models.device_registered(token))

    # Used for a device to be registered. Device submits unique token and name the device wants to be
    def post(self):
        jsonobject = json.loads(self.request.body)
        auth = jsonobject['auth']
        name = jsonobject['name']

        dev_reg = models.device_registered(auth)

        if (dev_reg == True):
            self.response.set_status(401)
            self.response.write('Device already registered')
        elif (dev_reg == False):
            models.register_pi(auth, name)
            self.response.write('Registered device')
        else:
            self.response.set_status(401)
            self.response.write('Incorrect Device ID')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/send-data', DataHandler),
    ('/register', RegisterHandler),
], debug=True)
