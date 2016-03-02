from datetime import datetime
import uuid

class Pi:

	def __init__(self, name, location):
		self.id = uuid.uuid4()
	  	self.name = name
	  	self.location = location
	  	self.registered_on = datetime.now()

