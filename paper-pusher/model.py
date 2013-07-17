import datetime

class Report():
	name = None
	variables = []
	description = None
	excel_workbooks = []
	
	def __init__(self, name = None):
		self.name = name
		
	def __string__(self):
		return name

class BasicVariable():
	
	name = None
	data_type = None
	is_transform = False
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		
	def __string__(self):
		return name
		
class TransformVariable(BasicVariable):
	
	# list of BasicVariable objects used to create this transform
	variables = []
	# operation to be executed on the variables
	transform_method = None
	arguments = []
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		self.is_transform = True

	# Compares two dates and returns an difference integer in days.
	# Returns null if either date passsed is not of type date
	def date_diff_days(self, oldest_date, newest_date):
		if type(newest_date) is datetime.date and type(newest_date) is datetime.date:
			date_diff = (newest_date - oldest_date).days
			return date_diff
		return None
		
	# Returns 1 if the cell_value begins with the specified string
	# Returns 0 if it does not
	# Return Null if a cell value is blank
	def begins_with(self, cell_values, begins_with):
	
		begins_with = str.lower(begins_with)
		
		for cell_value in cell_values:
			cell_value = str.lower(cell_value)
			if cell_value is None:
				return None
			elif not cell_value.startswith(begins_with):
				return 0
				
		return 1
	
	# Takes a list of cell values and determines if they are empty or not.
	# If one of the cell values passed is empty, returns 0, otherwise
	# returns 1, indicating the cell values are not empty
	def not_empty(self, cell_values):

		for cell_value in cell_values:
			cell_value = str.lower(cell_value).strip()
			if cell_value == None or cell_value == "":
					return 0
		return 1
		
class ExcelWorkbookContainer():
	path = None
	workbook = None
	worksheet_index_header_row_num = {}
	
	def __init__(self, path, workbook):
		self.workbook = workbook
		self.path = path
		self.generate_csv_file_from_excel_worksheets = {}