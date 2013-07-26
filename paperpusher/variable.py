import datetime
import pandas as pd
from xlsxwriter.workbook import Workbook
from paperpusher import spreadsheet
	
class SummaryVariable():
	"""Directions for how to summarize a given varaible
		
		Attributes:
			name: The summary variable's name
			variables: a list of variables
			methods: A list of dictionaries, with each dictionary
				defining a method in the form
				
				{
					method : method_name,
					objective_values: [objective_value],
					objective_must_be : must_be_string
				}
			conditions : [list] a list of lists of conditions in the form:
			
				[ [condition_1, condition_2], [condition_3] ]
				
				where all conditions in one set of conditions must be met. Using the above example we would interpret:
				
					Condition one and two must be met, or condition three must be met
			
			method_spreadsheet_position: [dictionary] dictionary in the form 
				
				{"Method print friendly name" : [row number, column number]}

				where the row and column number correspond to the position of the method display name in the spreadsheet
			name_spreadsheet_position: [list] list in the form
			
				[row_number, column number]
				
				for the position of the summary variable name in the spreadsheet
	"""
	
	def __init__(self, name, variables = [], methods = []):
		self.name = name
		self.variables = variables # a list of variables
		self.methods = methods
		
		# location of above attributes in the spreadsheet
		self.method_spreadsheet_position = {} # {method_name : [row_number, column_number]}
		self.name_spreadsheet_position = None # integer row number
		
		self.conditions = []
		
	def apply_method(self, data_frame, method_name):
		"""Applied the method specified by string to this variable
			
			Args:
				data_frame: A pandas dataframe object
				method_name: string representing one of the SummaryVariable analytic methods
				
			Returns:
				Returns the return value of a specified method. If no method matches
				the string, returns null.
		"""
		
		# apply conditions
		data_frame = self.apply_conditions(data_frame)
		
		if method_name == "min":
			return self.min(data_frame)
		elif method_name == "max":
			return self.max(data_frame)
		elif method_name == "mean":
			return self.mean(data_frame)
		elif method_name == "median":
			return self.median(data_frame)
		elif method_name == "sum":
			return self.sum(data_frame)
		elif method_name == "percent_of_sum":
			return self.percent_of_sum(data_frame)
		elif method_name == "percent_of_average":
			return self.percent_of_average(data_frame)
		elif method_name == "percent_of_obs":
			return self.percent_of_obs(data_frame)
			
		return None
		
	def apply_conditions(self, data_frame):
		"""Returns a subset of the data frame based on the conditions specified
			Args:
				data_frame: Pandas data frame
			Returns:
				Subset of pandas data frame. If no where clause, the original data_frame is returned
		"""
		
		if len(self.conditions) > 0:
			for condition_group in self.conditions:
				for condition in condition_group:	
					if condition.variable_must_be == "equal":
						data_frame = data_frame[data_frame[condition.variable_name] ==  condition.variable_values[0]]
					elif condition.variable_must_be == "less_than":
						data_frame = data_frame[data_frame[condition.variable_name] <  condition.variable_values[0]]
					elif condition.variable_must_be == "greater_than_equal_to":
						data_frame = data_frame[data_frame[condition.variable_name] >=  condition.variable_values[0]]
		
		return data_frame
		
	def get_method_display_name(self, method_name):
		"""Returns a user friendly display name for the method
			Args:
				method_name: a string method name corresponding to a summary method
			Returns:
				A friendly method display name
		"""
			
		if method_name == "min":
			return "Minimum"
		elif method_name == "max":
			return "Maximum"
		elif method_name == "mean":
			return "Average"
		elif method_name == "median":
			return "Median"
		elif method_name == "sum":
			return "Sum"
		elif method_name == "percent_of_sum" or method_name == "percent_of_average":
			return "Percent of " + self.variables[1]
		elif method_name == "percent_of_obs":
			return "Percent of observations"
		
		return method_name
		
	def get_objective_display_text(self, objective_must_be, objective_values):
		"""Returns a display string for the objective requirement
			Args:
				objective_must_be: String must_be value
				objective_values: list of values for the objective
			Returns:
				Returns a string description of the objective requirement
		"""
		
		if objective_must_be == "equal":
			return "Equals " + str(objective_values[0])
		elif objective_must_be == "greater_than_equal_to":
			return "At least " + str(objective_values[0])
		elif objective_must_be == "less_than":
			return "Less than " + str(objective_values[0])
		elif objective_must_be == "between":
			return "Betweeen " + str(objective_values[0]) + " and " +  str(objective_values[1])
		elif objective_must_be == "in":
			return "In " + str(objective_values)
		elif objective_must_be == "not_in":
			return "Not in " + str(objective_values)
		return False
		
	def objective_met(self, variable_value, objective_values, objective_must_be):
		"""Determines if an objective was met
			Args:
				variable_value: The variable value
				objective_values: list of values for the objective
				objective_must_be: String must_be value
			Returns:
				True if the objective is met, false otherwise.
		"""
	
		if objective_must_be == "equal":
			if variable_value == objective_values[0]:
				return True
		elif objective_must_be == "greater_than_equal_to":
			if variable_value >= objective_values[0]:
				return True
		elif objective_must_be == "less_than":
			if variable_value < objective_values[0]:
				return True
		elif objective_must_be == "between":
			if variable_value > objective_values[0] and variable_value > objective_values[1]:
				return True
		elif objective_must_be == "in":
			if variable_value in objective_values:
				return True
		elif objective_must_be == "not_in":
			if variable_value not in objective_values:
				return True
		return False
		
	
	# evaluative methods	
	def min(self, data_frame):
		return data_frame[self.variables[0]].min()
	def max(self, data_frame):
		return data_frame[self.variables[0]].max()
	def mean(self, data_frame):
		return data_frame[self.variables[0]].mean()
	def median(self, data_frame):
		return data_frame[self.variables[0]].median()
	def sum(self, data_frame):
		return data_frame[self.variables[0]].sum()
	def percent_of_sum(self, data_frame):
		"""Returns sum of variable[0] divided by sum of variable[1]
		"""
		
		sum_variable_one = data_frame[self.variables[0]].sum()
		sum_variable_two = data_frame[self.variables[1]].sum()
		
		return (sum_variable_one/sum_variable_two)*100

	def percent_of_average(self, data_frame):
		"""Returns the average of variable[0] divided by average of variable[1]
		"""
		
		average_variable_one = data_frame[self.variables[0]].mean()
		average_variable_two = data_frame[self.variables[1]].mean()
		
		return (average_variable_one/average_variable_two)*100
		
	def percent_of_obs(self, data_frame):
		"""Returns the sum of variable[0] divided by the number of observations
		"""
		sum_variable_one = data_frame[self.variables[0]].sum()
		observations = len(data_frame.index)
		
		return (sum_variable_one/observations)*100
		
class Condition():
	""" Directives to restrict a data frame based on condition
	
		Attributes:
			name : [string] the name of the condition
			variable_must_be : [string] one of the must_be values
			variable_values : [list] a list of values to be evalutaed using the "variable_must_be" operator
	"""
	
	def __init__(self, name, variable_name, variable_must_be, variable_values = []):
		self.name = name
		self.variable_name = variable_name
		self.variable_must_be = variable_must_be
		self.variable_values = variable_values

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