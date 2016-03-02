#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import ast
from models import ResultSet
from models import Result

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to jawsfi')

class DataHandler(webapp2.RequestHandler):
	def post(self):
		jsonobject = json.loads(self.request.body)
		pythonobject = ast.literal_eval(jsonobject)

		if jsonobject:
			result_set = ResultSet()
			result_set_key = result_set.put()

			
			print type(jsonobject)
			for key, value in pythonobject.iteritems():
				db_result = Result(mac_address=key, signal=value, result_set=result_set_key)
				db_result.put()

			self.response.write('Should of put items in data store')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/send-data', DataHandler)
], debug=True)
