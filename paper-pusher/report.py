class Report():
	name = None
	variables = []
	
	def __init__(self, name):
		self.name = name
		
	def __string__(self):
		return name

class BasicVariable():
	
	name = None
	data_type = None
	is_composite = False
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		
	def __string__(self):
		return name
		
class CompositeVariable(BasicVariable):
	
	# list of BasicVariable objects used to create this composite
	variables_composite_made_of = []
	# operation to be executed on the variables
	composite_method = None
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		self.is_composite = True

	# Compares two dates and returns an difference integer in days.
	# Returns null if either date passsed is not of type date
	def date_diff_days(self, oldest_date, newest_date):
		if type(newest_date) is datetime.date and type(newest_date) is datetime.date:
			date_diff = (newest_date - oldest_date).days
			return date_diff
		return None