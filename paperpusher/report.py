from paperpusher.variable import BasicVariable, TransformVariable, SummaryVariable
from xlsxwriter.workbook import Workbook
import pandas as pd
import csv

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
			# make a new worksheet for this summary section
			worksheet = workbook.add_worksheet(summary_section.name)
			# get the master csv data set
			data_frame = pd.read_csv(self.path_to_master_csv_file)
			
			row_num = 0
			col_num = 0
			
			for summary_variable in summary_section.summary_variables:
				col_num = 0
				
				# write the summary variable name
				variable_header_format = workbook.add_format({'bold': True, 'bg_color': '#DDDDDD'})
				variable_header_format.set_border(style=1)
				variable_header_format.set_align('center')
				variable_header_format.set_align('vcenter')
				
				# header names
				worksheet.merge_range(row_num, col_num + 1, row_num, 3, summary_variable.name, variable_header_format)
				row_num = row_num + 1
				
				# sub headers
				method_header_format = workbook.add_format({'bold': False,'bg_color': '#EEEEEE'})
				method_header_format.set_border(style=1)
				method_header_format.set_align('center')
				method_header_format.set_align('vcenter')
						
				worksheet.write(row_num, 1, "Value", method_header_format)
				worksheet.write(row_num, 2, "Objective", method_header_format)
				worksheet.write(row_num, 3, "Objective met", method_header_format)

				row_num = row_num + 1
				
				for variable in summary_variable.variables:
					# write the method names first
					for method in summary_variable.methods:

						method_name = method['method']
						method_display_name = summary_variable.get_method_display_name(method_name)
						worksheet.write(row_num, col_num, method_display_name, method_header_format)
						row_num = row_num + 1
						
					col_num = 1
					
					# roll back the row num
					row_num = row_num - len(summary_variable.methods)
						
					# now write the method values
					for method in summary_variable.methods:
					
						method_name = method['method']
						
						summary_variable_value = summary_variable.apply_method(data_frame, method_name)
						
						# write the summary variable value to the worksheet
						summary_variable_value_format = workbook.add_format({'bold': False})
						summary_variable_value_format.set_border(style=1)
						summary_variable_value_format.set_align('center')
						summary_variable_value_format.set_align('vcenter')
						
						worksheet.write(row_num, col_num, summary_variable_value, summary_variable_value_format)
						
						# objectives
						if 'objective_values' in method and 'objective_must_be' in method:
							objective_values = method['objective_values']
							objective_must_be = method['objective_must_be']
						
							# objective description
							col_num = col_num + 1
							objective_description = summary_variable.get_objective_display_text(objective_must_be, objective_values)
							worksheet.write(row_num, col_num, objective_description, summary_variable_value_format)
							
							# objective met
							col_num = col_num + 1
							objective_met = summary_variable.objective_met(summary_variable_value, objective_values, objective_must_be)
							if objective_met:
								summary_variable_value_format = workbook.add_format({'bold': True, 'color': '#008800', 'bg_color' : "#DDFFDD"})
								summary_variable_value_format.set_border(style=1)
								summary_variable_value_format.set_align('center')
								summary_variable_value_format.set_align('vcenter')
								worksheet.write(row_num, col_num, "Yes", summary_variable_value_format)
							else:
								summary_variable_value_format = workbook.add_format({'bold': True, 'color': '#FF0000', 'bg_color' : "#FFDDDD"})
								summary_variable_value_format.set_border(style=1)
								summary_variable_value_format.set_align('center')
								summary_variable_value_format.set_align('vcenter')
								worksheet.write(row_num, col_num, "No", summary_variable_value_format)
							
						else:
							# no objectives so put in "-"
							col_num = col_num + 1
							worksheet.write(row_num, col_num, "---", summary_variable_value_format)
							col_num = col_num + 1
							worksheet.write(row_num, col_num, "---", summary_variable_value_format)
						
						row_num = row_num + 1
						col_num = 1
				
				row_num = row_num + 2
				
		# insert the raw data worksheet as the last worksheet in the workbook
		self.insert_raw_data_worksheet("Raw data", workbook)
				
	def insert_raw_data_worksheet(self, worksheet_name, workbook):
	
		# make a new worksheet in this workbook
		worksheet = workbook.add_worksheet(worksheet_name)
		
		# load the master csv data
		master_csv = open(self.path_to_master_csv_file, 'r')
		master_csv_reader = csv.reader(master_csv, delimiter=',')
		
		# write the csv data to the worksheet
		for row, data in enumerate(master_csv_reader):
			worksheet.write_row(row, 0, data)
		
		master_csv.close()
					
class SummarySection():
	"""Variable names and methods for an outputted summary section of a report
		
		Attributes:
			name: Name of the summary section
			summary_variables: A list of SummaryVariable objects
	"""
	
	def __init__(self, name, summary_variables = []):
		self.name = name
		self.summary_variables = summary_variables