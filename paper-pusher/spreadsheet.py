import csv
import xlrd
import re


# 
def append_excel_worksheet_to_csv(worksheet, datemode, csv_file, variable_definitions, excel_header_row_number = 0, write_header = True):
	
	# this is stuff that should be appeneded to every row
	#region_name = clients_worksheet.region_name
	#case_manager_name = clients_worksheet.case_manager_name

	#csv_file = open(csv_file_path, 'a', newline='\n', encoding="utf-8")
	csv_writer = csv.writer(csv_file)
	
	# get the starting row number based on whether we 
	# want to print the header or not 
	excel_starting_row_num = excel_header_row_number	
	if not write_header:
		excel_starting_row_num = excel_header_row_number + 1
		
	# header names and column numbers for the csv and Excel file
	csv_header_column_numbers = get_variable_column_numbers(0, csv_file) # TODO the csv file might not have any header columns yet
	excel_header_column_numbers = get_variable_column_numbers(excel_header_row_number, worksheet)
	
	for row_num in range(worksheet.nrows):
		
		# list of data to be entered into the row
		row_insert = []
			
		if row_num >= excel_starting_row_num:

			for variable_name in variable_definitions:
				col_num = excel_header_column_numbers[variable_name]
				data_type = variable_definitions[variable_name]['data_type']

				cell_value = worksheet.cell(row_num,col_num).value
				
				# check for date columns. We enforce row_num > 1 as to not apply 
				# the date checking to the header
				if data_type == 'date' and row_num > 1:	
					cell_value = excel_date_to_string(cell_value, datemode)
					
				# string non-numbers from numeric entries
				elif data_type == 'numeric' and row_num > 1:	
					cell_value = re.sub(r'[^\d.]+', "", str(cell_value))

				# insert the cell value
				row_insert.append(cell_value)
					
			# add the composite variables and the 
			# "Region" and "Case manager" headers
			if write_header:
				# headers
				for composite_var_name in settings.composite_variables:
					row_insert.append(composite_var_name)
				row_insert.append("Region")
				row_insert.append("Case manager")
			else:
				# values
				for composite_var_name in settings.composite_variables:
					composite_var = settings.composite_variables[composite_var_name]
					composite_var_type = composite_var['type']
					composite_var_variables = composite_var['variables'] # variable names the composite is made up of
					
					# get the column numbers for each of the composite variables
					composite_var_columns = []
					header_names = composite_var['variables']
					for header_name in header_names:

						header_col_num = case_file_headers[header_name]['col_num']
						composite_var_columns.append(header_col_num)
					
					# date_diff
					if composite_var_type == 'date_diff':
						# try to convert the date string in form m/d/yyyy to a date
						try:
							# convert the Excel date to string
							date_one = excel_date_to_string(worksheet.cell(row_num,composite_var_columns[0]).value, datemode)
							date_two = excel_date_to_string(worksheet.cell(row_num,composite_var_columns[1]).value, datemode)
							
							# then convert back to a Python. We use the excel_date_to_string() function first so we can
							# check for weird formatting and entries that should be turned to null
							date_one = datetime.datetime.strptime(date_one, "%m/%d/%Y").date()
							date_two = datetime.datetime.strptime(date_two, "%m/%d/%Y").date()
							
							row_insert.append(date_diff_days(date_one, date_two))
						except:
							row_insert.append(None)
							
					# boolean_begins_with
					elif composite_var_type == 'boolean_begins_with':
						begins_with = composite_var['begins_with']
						if worksheet.cell(row_num,composite_var_columns[0]).value != None and worksheet.cell(row_num,composite_var_columns[0]).value != "":
							var_value = str.lower(worksheet.cell(row_num,composite_var_columns[0]).value)
							
							if var_value.startswith(begins_with):
								row_insert.append(1)
							else:
								row_insert.append(0)
						else:
							row_insert.append(None)
					
					# boolean_not_null
					elif composite_var_type == 'boolean_not_null':
						if worksheet.cell(row_num,composite_var_columns[0]).value != None:
							var_value = str.lower(str(worksheet.cell(row_num,composite_var_columns[0]).value))
							if var_value != None and var_value != "":
								row_insert.append(1)
							else:
								row_insert.append(0)
						else:
							row_insert.append(None)
					else:
						row_insert.append(None)
					
				#row_insert.append(region_name)
				#row_insert.append(case_manager_name)
					
			# add the row to the csv file
			csv_writer.writerow(row_insert)
			
			# don't include the header after the first row
			write_header = False

	csv_file.close()
	
# returns a map of the form {header_variable_name : column_number}
def get_variable_column_numbers(header_row_num, spreadsheet):

	header_name_column_number = {}
	
	# Excel worksheet
	if type(spreadsheet) == xlrd.sheet.Sheet:
		for column_number in range(spreadsheet.ncols):
			header_name = spreadsheet.cell(header_row_num,column_number).value
			header_name_column_number[header_name] = column_number
			
	# otherwise it's a csv file
	else:
		current_row = 0
		for row in spreadsheet:
			
			if current_row == header_row_num:
				column_number = 0
				for header_name in row:
					header_name_column_number[header_name] = column_number
					column_number = column_number + 1
				break
				
			else:
				current_row = current_row + 1
	
	return header_name_column_number