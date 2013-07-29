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
		self.path_to_master_csv_file = "." # the master CSV to build this report from
		self.groups = {} # map in the form {group_name : group_object} of groups that can be applied to summary variables
		
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
			
			# display the objectives first, if there are any
			first_objective = True
			for objective in summary_section.objectives:
				col_num = 0
				# objectives
				if first_objective:
					# objectives header
					objectives_header_format = workbook.add_format({'bold': True, 'bg_color': '#DDDDDD'})
					objectives_header_format.set_border(style=1)
					objectives_header_format.set_align('center')
					objectives_header_format.set_align('vcenter')
					worksheet.merge_range(row_num, col_num, row_num, 1, "Objectives", objectives_header_format)
					
					row_num = row_num + 1
					
					# subheader
					objectives_subheader_format = workbook.add_format({'bold': False, 'bg_color': '#EEEEEE'})
					objectives_subheader_format.set_border(style=1)
					objectives_subheader_format.set_align('center')
					objectives_subheader_format.set_align('vcenter')
					
					worksheet.write(row_num, col_num, "Objective", objectives_subheader_format)
					worksheet.write(row_num, col_num + 1, "Met", objectives_subheader_format)
					
					# headers for objective, status, and difference
					first_objective = False
					row_num = row_num + 1
				
				# values
				summary_variable_value_format = workbook.add_format({'bold': False})
				summary_variable_value_format.set_border(style=1)
				summary_variable_value_format.set_align('center')
				summary_variable_value_format.set_align('vcenter')
					
				# objective name
				objective_name = objective.name
				worksheet.write(row_num, col_num, objective_name, summary_variable_value_format)
				
				summary_variable_value = objective.summary_variable.apply_method(data_frame, objective.method, objective.group)
				
				# objective met
				col_num = col_num + 1
				objective_met = objective.objective_met(summary_variable_value, objective.objective_values, objective.objective_must_be)
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
					
				row_num = row_num + 1
					
			# if we have at least one objective, add another row before the summary variables
			if not first_objective:
				row_num = row_num + 1

			# display the summary variable output
			for summary_variable_name in summary_section.summary_variables:
				summary_variable = summary_section.summary_variables[summary_variable_name]
				col_num = 0
				
				# write the summary variable name
				variable_header_format = workbook.add_format({'bold': True, 'bg_color': '#DDDDDD'})
				variable_header_format.set_border(style=1)
				variable_header_format.set_align('center')
				variable_header_format.set_align('vcenter')
				# save the row and column number this header was inputted into in the report spreadsheet
				summary_variable.name_spreadsheet_position = [row_num, col_num]
				
				# header names
				num_cells_to_merge = len(summary_variable.methods)
				worksheet.merge_range(row_num, col_num, row_num, num_cells_to_merge, summary_variable.name, variable_header_format)
				row_num = row_num + 1
				
				# sub headers
				subheader_format = workbook.add_format({'bold': False,'bg_color': '#EEEEEE'})
				subheader_format.set_border(style=1)
				subheader_format.set_align('center')
				subheader_format.set_align('vcenter')
				
				worksheet.write(row_num, col_num, "Group", subheader_format)
				
				col_num = 1
				
				# write the method names first
				for method_name in summary_variable.methods:
					method_display_name = summary_variable.get_method_display_name(method_name)
					worksheet.write(row_num, col_num, method_display_name, subheader_format)
					# save the row and column number in the outputed report spreadsheet for the method
					summary_variable.method_spreadsheet_position['method_name'] = [row_num, col_num]
					
					col_num = col_num + 1
					
				row_num = row_num + 1
				
				# write the summary variable value to the worksheet
				summary_variable_value_format = workbook.add_format({'bold': False})
				summary_variable_value_format.set_border(style=1)
				summary_variable_value_format.set_align('center')
				summary_variable_value_format.set_align('vcenter')
					
				# now write the method values
				for group in summary_variable.groups:
					col_num = 0
					# write the group name first
					worksheet.write(row_num, col_num, group.name, summary_variable_value_format)
					col_num = col_num + 1
					# roll back the column num
					col_num = 1
					
					for method_name in summary_variable.methods:
						summary_variable_value = summary_variable.apply_method(data_frame, method_name, group)
						worksheet.write(row_num, col_num, summary_variable_value, summary_variable_value_format)
						col_num = col_num + 1
						
					row_num = row_num + 1
				
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
			name : [string] Name of the summary section
			summary_variables : [dictionary] A map of SummaryVariable objects where the key is the name of the summary variable
			objectives: [list] A list of Objective objects
	"""
	
	def __init__(self, name, summary_variables = None, objectives = None):
		self.name = name
		
		if summary_variables == None:
			summary_variables = {}
		if objectives == None:
			objectives = []
		
		self.summary_variables = summary_variables
		self.objectives = objectives
		
class Objective():
	""" An objective to be met for a summary goal method value
	
		Attributes:
			group : [Group] a group for this objective. If null group is "All observations"
			method : [string] a method for the objective value
			summary_variable : [SummaryVariable] the summary variable to be evaluated
			objective_must_be : [string] one of the must_be values
			objective_values : [list] a list of the objective values to be evaluated
	"""
	
	def __init__(self, name, method, summary_variable, objective_must_be, objective_values, group = None):
		self.name = name
		self.group = group
		self.method = method
		self.summary_variable = summary_variable
		self.objective_must_be = objective_must_be
		self.objective_values = objective_values
		
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
		
class Chart():
	def __init__(self, name, summary_variable, method, groups = None):
		self.name = name
		self.summary_variable = summary_variable
		self.method = method
		if groups == None:
			groups = []
		self.groups = groups