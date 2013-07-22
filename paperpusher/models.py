import datetime
import pandas as pd
from xlsxwriter.workbook import Workbook
from paperpusher import spreadsheet_helper

class Report():
	
	def __init__(self, name = None):
		self.name = name
		self.variables = []
		self.description = None
		self.additional_header_names = [] # additional header names not defined in the report.json file, such as an ID or a constant
		self.summary_sections = []
		self.path_to_master_csv_file = None # the master CSV to build this report from
		
	def __string__(self):
		return name
		
	def add_variables_by_header_names(self, header_names):
		"""Creates new variables based on header names.
		
			Generates and appends BasicVariable objects to the Report.variables
			attribute based on a list of header string names.
				Args:
					header_names: A list of string header variable names.
		"""
		for header_name in header_names:
			variable = BasicVariable(header_name)
			variables.append(variable)
			
	def generate_report(self):
	
		workbook = Workbook(self.name + ".xlsx")
		
		for summary_section in self.summary_sections:
			worksheet = workbook.add_worksheet(summary_section.name)
			
			# get the master csv data set
			data_frame = pd.read_csv(self.path_to_master_csv_file)
			
			row_num = 0
			for summary_variable in summary_section.variables:
				
				# write the variable name
				worksheet.write(0, row_num, summary_variable.name)
				row_num = row_num + 1
				
				column_num = 0
				for method in summary_variable.methods:
				
					# get the summary value
					method_name = method["method"];
					summary_value = summary_variable.apply_method(data_frame, method_name)
					
					worksheet.write(column_num, row_num, method_name)
					column_num + 1
					
					worksheet.write(column_num, row_num, summary_variable.name)
					column_num + 1
					
				row_num = row_num + 2
					
		
class SummarySection():
	"""Variable names and methods for an outputted summary section of a report
		
		Attributes:
			name: Name of the summary section
			summary_variables: A list of SummaryVariable objects
	"""
	
	def __init__(self, name, summary_variables = None):
		self.name = name
		self.summary_variables = summary_variables
	
class SummaryVariable():
	"""Directions for how to summarize a given varaible
		
		Attributes:
			name = The summary variable's name
			methods = A list of dictionaries, with each dictionary
				defining a method in the form
				
				TODO: this is in flux
				{
					"method" : method_name,
					"threshold_value": threshold_value,
					"must_be_greater_than_equal_to" : true_or_false
				}
	"""
	
	def __init__(self, name, methods = None, variables = None):
		self.name = name
		self.variables = variables # a list of variables
		self.methods = methods
		self.where_clause = {}
		
	def apply_method(self, data_frame, method_name):
		"""Applied the method specified by string to this variable
			
			Args:
				data_frame: A pandas dataframe object
				method_name: string representing one of the SummaryVariable analytic methods
				
			Returns:
				Returns the return value of a specified method. If no method matches
				the string, returns null.
		"""
		
		# TODO: apply the where clause
		
		if method_name == "min":
			return self.min(data_frame)
		elif method_name == "max":
			return self.max(data_frame)
		elif method_name == "mean":
			return self.mean(data_frame)
		elif method_name == "median":
			return self.median(data_frame)
			
		return None
		
	def min(self, data_frame):
		return data_frame[self.name].min()
		
	def max(self, data_frame):
		return data_frame[self.name].max()
		
	def mean(self, data_frame):
		return data_frame[self.name].mean()
		
	def median(self, data_frame):
		return data_frame[self.name].median()
	
	#TODO: impelment these methods
	def percent_of_total_obs(self, data_frame):
		return None
	def percent_of_not_null_obs(self, data_frame):
		return None

class BasicVariable():
	"""Model for a basic, non-transformed, variable
	
	Represents the model for a basic report variable, such as "First name" or "Sex".
		Attributes:
			name: The name of the variable, such as "First name". This name should correspond
				with the header column name used in a user's spreadsheet.
			data_type: The data type for this variable. Data types are
				* date
				* string
				* integer
				* float
				* boolean
			is_transform: A boolean attribute indicating whether this variable is a basic, unmodified
				variable such as "First name", or if the variable requires some transformation - such
				as being the composite of two or more variables or having some mathematical operation
				performed on it.
	"""
	
	def __init__(self, name, data_type = None):
		self.name = name
		self.data_type = data_type
		self.is_transform = False
		
	def __string__(self):
		return name
		
class TransformVariable(BasicVariable):
	"""Model for a transformed variable
	
	The TransformVariable extends the BasicVariable and represents a variable that is 
	either a composite or requires some type of mathematical transformation, using one
	or more variables from a user's spreadsheet.
		Attributes:
			variables: A list of variable objects used to create the transformed variable
			transform_method: A string indicating which transform method (one of the methods on this
				TransformVariable object) that should be used. For example, "date_diff_days".
			arguments: A list of argument other than variable names to be passed to the transform method.
				For example, using the "begins_with" method the arugments attribute might be ["begins with this?"]
	"""
	
	def __init__(self, name, data_type):
		self.name = name
		self.data_type = data_type
		self.is_transform = True
		self.variables = []
		self.transform_method = None
		self.arguments = []

	def date_diff_days(self, oldest_date, newest_date):
		"""
		Compares two dates and returns an difference integer in days.
			Args:
				oldest_date: The oldest datetime object
				newst_date: The newest datetime object
			Returns:
				Returns null if either date passsed is not of type date, otherwise returns
				an integer value indicate the number of days between the two dates.
		"""
		if type(newest_date) is datetime.date and type(newest_date) is datetime.date:
			date_diff = (newest_date - oldest_date).days
			return date_diff
		return None
		

	def begins_with(self, cell_values, begins_with):
		"""Determines if a set of cell contents begins with a given string.
		
			Args:
				cell_values: A list of cell values from a spreadsheet
				begins_with: A string to check if each cell value begins with
			Returns:
				Returns an integer 1 to indcate all cells do begin with the passed value, an integer
				0 to indicate one or more of the cells do not begin with the passed value, and returns
				null if one or more of the passed cell_contents is is null.
		"""
	
		begins_with = str.lower(begins_with)
		
		for cell_value in cell_values:
			cell_value = str.lower(cell_value)
			if cell_value is None:
				return None
			elif not cell_value.startswith(begins_with):
				return 0
				
		return 1
	
	def not_empty(self, cell_values):
		"""Determines if the contents of cell values are empty or not
		
		If one of the cell values passed is empty, returns 0, otherwise
		returns 1, indicating the cell values are not empty.
			Args:
				cell_values: A list of cell values from a spreadsheet.
			Returns:
				An integer (0 or 1) indicating a cell is not empty (1) 
				or is empty (0).
		"""

		for cell_value in cell_values:
			cell_value = str.lower(cell_value).strip()
			if cell_value == None or cell_value == "":
					return 0
		return 1
		
class CsvFileContainer():
	
	def __init__(self, path, additional_cell_values = None):
		self.path = path
		self.additional_cell_values = additional_cell_values # list of cell values to append as extra columns at the end of each row
		
class ExcelWorksheetContainer():	
	
	def __init__(self, worksheet, datemode, header_row_number):
		self.worksheet = worksheet
		self.datemode = datemode
		self.header_row_number = header_row_number