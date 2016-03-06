from google.appengine.ext import ndb

class Pi(ndb.Model):
    """A model for storing Rasberry Pi devices"""
    pi_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    activated = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

class Result(ndb.Model):
	mac_address = ndb.StringProperty(required=True)
	signal = ndb.IntegerProperty(required=True)
	result_set = ndb.KeyProperty(required=True)

class ResultSet(ndb.Model):
	# Standard time needs to be in UTC and represents the time of the results
	# e.g. 06/03/2016 12:00...12:10...12:20...12:30 irrespective of what time it was 
	# actually recieved and processed
	standard_time = ndb.DateTimeProperty() 
	created = ndb.DateTimeProperty(auto_now_add=True)

def get_num_unique_sets():
	qry = ResultSet.query()
	return qry.count()

def get_unique_results():
	qry = Result.query()
	return qry.count()

def get_last_submission():
	qry = ResultSet.query().order(-ResultSet.created)
	results = qry.fetch(limit=1)
	if results:
		return results[0].created
	else:
		return None

def device_registered(token):
	qry = Pi.query(Pi.pi_id==token)
	results = qry.fetch(limit=1)
	if results:
		return results[0].activated
	else:
		return None

def register_pi(token, name):
	qry = Pi.query(Pi.pi_id==token)
	results = qry.fetch(limit=1)
	results[0].name = name
	results[0].activated = True
	results[0].put()