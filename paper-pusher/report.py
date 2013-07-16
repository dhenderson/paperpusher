

class Report():
	name = None
	report_variables = []
	
	def __init__(self, name, report_variables):
		self.name = name
		self.report_variables = report_variables
		
	def __string__(self):
		return name

class BasicVariable():
	
	name = None
	data_type = None
	is_composite = False
	output_column_num = None
	input_column_num = None
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		
	def __string__(self):
		return name
		
	# Converts an Excel date into the date format m/d/YYYY
	def excel_date_to_string(self, cell_value, datemode):
		# if the type is a float, then conver to date with xldate_as_typle
		if type(cell_value) is float and cell_value > 1000:
			date = xlrd.xldate_as_tuple(cell_value, datemode)
			#cell_value = datetime.datetime(date[0], date[1], date[2])
			cell_value = str(date[1]) + "/" + str(date[2]) + "/" + str(date[0])
		else:
			# we didn't convert to a date, so set the cell value to null
			cell_value = None
			
		return cell_value
		
class CompositeVariable(BasicVariable):
	
	# list of BasicVariable objects used to create this composite
	variables = []
	# operation to be executed on the variables
	operation = None
	
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