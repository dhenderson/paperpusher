from paperpusher.variable import BasicVariable, SummaryVariable, TransformVariable

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
			
	def write_excel_summary_report(self):

		workbook = Workbook(self.name + ".xlsx")
		
		for summary_section in self.summary_sections:
			worksheet = workbook.add_worksheet(summary_section.name)
			
			# get the master csv data set
			data_frame = pd.read_csv(self.path_to_master_csv_file)
			
			for summary_variable in summary_section.variables:
				
				for method in summary_variable.methods:
				
					method_name = method["method"];
					#target_value = method["target_value"]
					#must_be_greater_than_equal_to = method["must_be_greater_than_equal_to"]
					
					summary_value = summary_variable.apply_method(data_frame, method_name)
					
					
	def write_doc():
		doc = open(settings.word_doc, 'w')
		doc.write("<html><body>")
		doc.write("<p>This is a paragraph</p>")
		doc.write("<p>Second paragraph</p>")
		doc.write("<img src='report_images/cat.jpg' />")
		doc.write("</body></html>")
		doc.close()