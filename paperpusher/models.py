import datetime

class Report():
	
	def __init__(self, name = None):
		self.name = name
		self.variables = []
		self.description = None
		self.excel_workbooks = []
		self.additional_header_names = [] # additional header names not defined in the report.json file, such as an ID or a constant
		
	def __string__(self):
		return name
		
	def add_variables_by_header_names(self, header_names):
		""" Creates new variables based on header names.
		
			Generates and appends BasicVariable objects to the Report.variables
			attribute based on a list of header string names.
				Args:
					header_names: A list of string header variable names.
		"""
		for header_name in header_names:
			variable = BasicVariable(header_name)
			variables.append(variable)
			
	def write_excel_report(self):

		report_xlsx = Workbook(settings.report_xlsx)
		summary_worksheet = report_xlsx.add_worksheet("Summary")
		
		# get the master csv data set
		d = pd.read_csv(settings.master_csv)
		
		# Table headers
		summary_worksheet.write(0, 0, '')
		summary_worksheet.write(0, 1, 'All')
		starting_region_col_num = 2
		datasets = {'All' : d}
		for region_name in settings.region_names:
			summary_worksheet.write(0, starting_region_col_num, region_name)
			starting_region_col_num = starting_region_col_num + 1
			
			# get a subset for this region
			datasets[region_name] = d[d['Region'] == region_name]
		
		summary_row = 1
		summary_column = 0
		summary_worksheet.write(summary_row, summary_column, 'HOMES ID')
		for dataset_name in datasets:
			dataset = datasets[dataset_name]
			summary_worksheet.write(summary_row, summary_column, str(dataset['HOMES ID'].mean()))
			summary_column = summary_column + 1
		summary_row = summary_row + 1
		
		return d
		
	def write_doc():
		doc = open(settings.word_doc, 'w')
		doc.write("<html><body>")
		doc.write("<p>This is a paragraph</p>")
		doc.write("<p>Second paragraph</p>")
		doc.write("<img src='report_images/cat.jpg' />")
		doc.write("</body></html>")
		doc.close()

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
		
class CsvFilesContainer():
	
	def __init__(self):
		csv_files = [] # list of csv files
		self.additional_cell_values = [] # list of cell values to append as extra columns at the end of row
		
class ExcelWorksheetContainer():	
	
	def __init__(self, worksheet, datemode, header_row_number):
		self.worksheet = worksheet
		self.datemode = datemode
		self.header_row_number = header_row_number