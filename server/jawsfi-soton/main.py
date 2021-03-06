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
        probes = models.get_probes()
        print probes
        probe_list = []

        for probe in probes:
            probe_list.append({'auth': probe.pi_id, 'name': probe.name})

        template_values = {'num_sets': models.get_num_unique_sets(),
                           'unique_results': models.get_unique_results(),
                           'last_result': models.get_last_submission(),
                           'probes': probe_list}


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
        print self.request.body

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

class GetRegisteredProbesHandler(webapp2.RequestHandler):
    def get(self):
        probes = models.get_probes()
        list = []

        for probe in probes:
            list.append({'id': probe.pi_id, 'name': probe.name})

        output = {'probes': list}
        self.response.out.write(json.dumps(output))



class GetAvailableResultsHandler(webapp2.RequestHandler):
    def get(self):
        sets = models.get_sets_avail()

        output = {}
        times = []

        for result in sets:
            times.append(str(result.standard_time))

        output['times'] = times
        self.response.out.write(json.dumps(output))

    def post(self):
        print 'something'
        print self.request.body

        jsonobject = json.loads(self.request.body)
        time = datetime.datetime.strptime(jsonobject['time'], "%Y-%m-%d %H:%M:%S")
        auth = jsonobject['auth']

        num = models.get_num_results(auth, time)
        output = {'standard_time': str(time), 'number': num}
        self.response.out.write(json.dumps(output))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/send-data', DataHandler),
    ('/register', RegisterHandler),
    ('/avail', GetAvailableResultsHandler),
    ('/probes', GetRegisteredProbesHandler),
], debug=True)
