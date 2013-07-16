import csv
import xlrd
import re

def generate_csv_file_from_excel_worksheets(path_to_csv_file, report, excel_workbook_containers):
	
	# generate a new csv file with the headers from the report
	csv_file = generate_csv_file_with_headers(path_to_csv_file, report)
	
	# loop through Excel Workbooks pulling each Excel Worksheet as needed
	for excel_workbook_container in excel_workbook_containers:
		
		# loop through map of worksheet index numbers and header rows for each worksheet
		for worksheet_index in excel_workbook_container.worksheet_index_header_row_num:
		
			# pull the header row number for this worksheet 
			# using the worksheet_index as a key
			excel_header_row_num = excel_workbook_container.worksheet_index_header_row_num[worksheet_index]
			# get the worksheet from the workbook using xlrd's sheet_by_index() method
			excel_worksheet = excel_workbook_container.workbook.sheet_by_index(worksheet_index)
			
			# append the contents of this worksheet to the csv file
			append_excel_worksheet_to_csv(excel_worksheet, excel_workbook_container.workbook.datemode, path_to_csv_file, report, excel_header_row_num)
		

# Appends Excel worksheet values for the variables specified in the given report to a csv file 
def append_excel_worksheet_to_csv(excel_worksheet, excel_workbook_datemode, path_to_csv_file, report, excel_header_row_number):

	csv_file = open(path_to_csv_file, 'a', newline='')
	csv_writer = csv.writer(csv_file)
	
	# get the column numbers for the headers
	csv_header_column_numbers = get_variable_column_numbers(open(path_to_csv_file, 'rt'), 0)
	excel_header_column_numbers = get_variable_column_numbers(excel_worksheet, excel_header_row_number)
				
	for excel_row_num in range(excel_worksheet.nrows):
		
		# temporary list container for the row data
		row_insert = []
	
		if excel_row_num > excel_header_row_number:
			
			for variable in report.variables:
			
				# get the column number and variable name mapping for the csv file
				csv_col_num = csv_header_column_numbers[variable.name]
				excel_col_num = excel_header_column_numbers[variable.name]
				
				cell_value = excel_worksheet.cell(excel_row_num,excel_col_num).value
				
				# basic variable
				if not variable.is_composite:
					
					# since this is a basic variable, the header names in the Excel and CSV
					# will match, so get the Excel variable column number
					excel_col_num = excel_header_column_numbers[variable.name]
					
					cell_value = cleanup_excel_data(variable, cell_value, excel_workbook_datemode)
					
				# composite variable
				else:
					if variable.data_type == "date":
						old_date_variable_name = variable.variables_composite_made_of[0]
						new_date_variable_name = variable.variables_composite_made_of[1]
						
						old_date_variable_column_num = excel_header_column_numbers[old_date_variable_name]
						new_date_variable_column_num = excel_header_column_numbers[new_date_variable_name]
						
						old_date = excel_worksheet.cell(excel_row_num, old_date_variable_column_num).value
						new_date = excel_worksheet.cell(excel_row_num, new_date_variable_column_num).value
						
						# cleanup the dates before computing the difference
						old_date = cleanup_excel_data(variable, old_date, excel_workbook_datemode)
						new_date = cleanup_excel_data(variable, new_date, excel_workbook_datemode)
						
						if variable.composite_method == 'date_diff_days':
							cell_value = date_diff_days(old_date, new_date)
							
				# insert the cell value in the proper CSV column
				row_insert.insert(csv_col_num, cell_value)
			
			print("row_insert: " + str(row_insert))

			# write the row
			csv_writer.writerow(row_insert)

	# close the file
	csv_file.close()
	
# generates and returns a csv file with the headers variable
# names specified in the passed Report object
def generate_csv_file_with_headers(path_to_csv_file, report):

	csv_file = open(path_to_csv_file, 'w', newline='')
	csv_writer = csv.writer(csv_file)
	csv_headers = []
	
	for variable in report.variables:
		csv_headers.append(variable.name)
	
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
			header_name = spreadsheet.cell(header_row_num,column_number).value
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
	elif variable.data_type == 'numeric':	
		cell_value = re.sub(r'[^\d.]+', "", str(cell_value))
		
	return cell_value