import csv
import xlrd
import re
import datetime

#def generate_csv_file_from_excel_worksheets(path_to_csv_file, report, excel_workbook_containers):
def generate_master_csv(path_to_master_csv_file, report, csv_file_containers):
	"""
	Compiles a master csv file appending an arbitrary number of csv file contents
	pulling the variables specified by the Report object
	"""
	
	# generate a new csv file with the headers from the report
	master_csv_file = generate_csv_file_with_headers(path_to_master_csv_file, report)
	
	for csv_file_container in csv_file_containers:
	
		path_to_input_csv_file = csv_file_container.path
		# append the contents of this worksheet to the csv file
		append_csv_to_master_csv(path_to_input_csv_file, path_to_master_csv_file, report, csv_file_container.additional_cell_values)
		


#def append_excel_worksheet_to_csv(excel_workbook_container, worksheet_index, path_to_csv_file, report, excel_header_row_number):
def append_csv_to_master_csv(path_to_input_csv_file, path_to_master_csv_file, report, additional_cell_values):

	"""Appends a csv file to a master csv file
	
		Appends a csv file for the variables specified in the given report 
		to a master csv file with variable transformations
		
		Args:
			path_to_input_csv_file: path to the csv file we are appending to the master csv
			path_to_master_csv_file: path to the master csv file the first inputted csv is being appended to
			report: A paperpusher.models.Report object defining the variables to be pulled from the inputted csv
			additional_cell_values: A list of additional cell value constants to be added at the end of each row entry
	"""

	input_csv_file = open(path_to_input_csv_file, 'r')
	input_csv_file_reader = csv.reader(input_csv_file, delimiter=',')

	master_csv_file = open(path_to_master_csv_file, 'a', newline='')
	master_csv_writer = csv.writer(master_csv_file)
	
	# get the column numbers for the headers
	input_csv_header_column_numbers = get_variable_column_numbers(open(path_to_input_csv_file, 'rt'), 0)
	master_csv_header_column_numbers = get_variable_column_numbers(open(path_to_master_csv_file, 'rt'), 0)
				
	for input_csv_file_row in input_csv_file_reader:
		
		# temporary list container for the row data
		master_row_insert = []
	
		# skip the first row of the input csv file, as this is the header
		if input_csv_file_reader.line_num > 1:
		
			for variable in report.variables:
			
				master_csv_col_num = master_csv_header_column_numbers[variable.name]
				
				# basic variable
				if not variable.is_transform:
					# get the column number and variable name mapping for the csv file
					input_csv_col_num = input_csv_header_column_numbers[variable.name]
					cell_value = input_csv_file_row[input_csv_col_num]
					
				# transform variable
				else:
					
					if variable.transform_method == 'date_diff_days':
						
						try:
							old_date_variable_name = variable.variables[0]
							new_date_variable_name = variable.variables[1]
							
							old_date_variable_column_num = input_csv_header_column_numbers[old_date_variable_name]
							new_date_variable_column_num = input_csv_header_column_numbers[new_date_variable_name]
							
							old_date = input_csv_file_row[old_date_variable_column_num]
							new_date = input_csv_file_row[new_date_variable_column_num]
							
							if old_date != None and new_date != None:
								# turn the date string into python dates
								date_one = datetime.datetime.strptime(old_date, "%m/%d/%Y").date()
								date_two = datetime.datetime.strptime(new_date, "%m/%d/%Y").date()
							
								cell_value = variable.date_diff_days(date_one, date_two)
						except:
							cell_value = None

					elif variable.transform_method == 'not_empty':
						# loop through variables and get values
						var_cell_vals = []
						for variable_name in variable.variables:
							input_csv_col_num = input_csv_header_column_numbers[variable_name]
							input_var_cell_value = input_csv_file_row[input_csv_col_num]
							var_cell_vals.append(input_var_cell_value)
							
						cell_value = variable.not_empty(var_cell_vals)
						
					elif variable.transform_method == 'begins_with':
						begins_with = variable.arguments[0]
						
						# TODO: cleaup code repition with "not_empty" method above
						var_cell_vals = []
						for variable_name in variable.variables:
							input_csv_col_num = input_csv_header_column_numbers[variable_name]
							input_var_cell_value = input_csv_file_row[input_csv_col_num]
							var_cell_vals.append(input_var_cell_value)
						
						cell_value = variable.begins_with(var_cell_vals, begins_with)
							
				# insert the cell value in the proper CSV column
				master_row_insert.insert(master_csv_col_num, cell_value)
			
			for additional_cell_value in additional_cell_values:
				master_row_insert.append(additional_cell_value)
			
			print("row_insert: " + str(master_row_insert))

			# write the row to the master csv
			master_csv_writer.writerow(master_row_insert)

	# close the file
	master_csv_file.close()
	
# generates and returns a csv file with the headers variable
# names specified in the passed Report object
def generate_csv_file_with_headers(path_to_csv_file, report):

	csv_file = open(path_to_csv_file, 'w', newline='')
	csv_writer = csv.writer(csv_file)
	csv_headers = []
	
	for variable in report.variables:
		csv_headers.append(variable.name)
		
	for additional_header_name in report.additional_header_names:
		csv_headers.append(additional_header_name)
	
	csv_writer.writerow(csv_headers)
	csv_file.close()
	
	return csv_file
	
# Converts an Excel date into the date format m/d/YYYY
def excel_date_to_string(cell_value, datemode):
	
	# if the type is a float, then conver to date with xldate_as_typle
	if type(cell_value) is float and cell_value > 1000:
		date = xlrd.xldate_as_tuple(cell_value, datemode)
		#cell_value = datetime.datetime(date[0], date[1], date[2])
		cell_value = str(date[1]) + "/" + str(date[2]) + "/" + str(date[0])
	else:
		# we didn't convert to a date, so set the cell value to null
		cell_value = None
		
	return cell_value
	
# returns a map of the form {header_variable_name : column_number}
def get_variable_column_numbers(spreadsheet, header_row_num):

	header_name_column_number = {}
	
	# Excel worksheet
	if type(spreadsheet) == xlrd.sheet.Sheet:
		for column_number in range(spreadsheet.ncols):
			header_name = spreadsheet.cell(header_row_num,column_number).value.strip().replace('\n', '')
			header_name_column_number[header_name] = column_number
			
	# otherwise it's a csv file
	else:
		current_row = 0
		
		# get a csv writer for this csv spreadsheet
		csv_reader = csv.reader(spreadsheet, delimiter=',')
		for row in csv_reader:
			if current_row == header_row_num:
				
				column_number = 0
				for header_name in row:
					if header_name != None and header_name != '':
						header_name_column_number[header_name] = column_number
						column_number = column_number + 1
				
				break

			current_row = current_row + 1
				
		spreadsheet.close()
	
	return header_name_column_number
	
# cleans up Excel cell values based on the variable's data type
def cleanup_excel_data(variable, cell_value, datemode = None):
	# check for date columns. We enforce row_num > 1 as to not apply 
	# the date checking to the header
	if variable.data_type == 'date':
		cell_value = excel_date_to_string(cell_value, datemode)
		
	# string non-numbers from numeric entries
	elif variable.data_type == 'int' or variable.data_type == 'float':	
		cell_value = re.sub(r'[^\d.]+', "", str(cell_value))
		
	return cell_value
	
def excel_worksheet_to_csv(excel_worksheet, excel_header_row_number, datemode, path_to_csv_output, variables):
	"""Copies the contens of an Excel worksheet into a CSV file

		Args:
			excel_worksheet: an xlrd worksheet object
			excel_header_row_number: the header row number in the worksheet
			path_to_csv_output: the full path, including "name.csv" where the outputted csv should go
			datemode: an xlrd ojbect Excel workbook's datemode
			variables: BasicVariable objects, where each variable is a variable to 
				be transfered from the Excel to the CSV
	"""
	
	# get the header row numbers for each variable in the Excel spreadsheet
	excel_header_column_numbers = get_variable_column_numbers(excel_worksheet, excel_header_row_number)

	csv_file = open(path_to_csv_output, 'w', newline='')
	csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
	
	for row_num in range(excel_worksheet.nrows):
		
		insert_row = []
		# headers
		if row_num == excel_header_row_number:
			for variable in variables:
				if not variable.is_transform:
					cell_value = variable.name
					insert_row.append(cell_value)
			csv_writer.writerow(insert_row)
				
		# contents
		elif row_num > excel_header_row_number:
			for variable in variables:
				# ignore transformations here, we only want to copy raw data
				if not variable.is_transform:
					try:
					
						# since this is a basic variable, the header names in the Excel and CSV
						# will match, so get the Excel variable column number
						
						excel_col_num = excel_header_column_numbers[variable.name]
						
						cell_value = excel_worksheet.cell(row_num, excel_col_num).value
						cell_value = cleanup_excel_data(variable, cell_value, datemode)
						
					except:
						# this header key doesn't exist in the spreadsheet, so set the cell value to null
						cell_value = None
						
					insert_row.append(cell_value)
			csv_writer.writerow(insert_row)

	csv_file.close()