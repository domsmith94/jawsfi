from google.appengine.ext import ndb

class Pi(ndb.Model):
    """A model for storing Rasberry Pi devices"""
    pi_id = ndb.StringProperty(required=true)
    created = ndb.DateTimeProperty(auto_now_add=True)

class Result(ndb.Model):
	mac_address = ndb.StringProperty(required=true)
	signal = ndb.IntegerProperty(required=true)
	result_set = ndb.KeyProperty()

class ResultSet(ndb.Model):
	created = ndb.DateTimeProperty