import csv
import xlrd
import re


def append_excel_worksheet_to_csv(excel_worksheet, excel_workbook_datemode, path_to_csv_file, report, excel_header_row_number):

	csv_file = open(path_to_csv_file, 'a')
	csv_writer = csv.writer(csv_file)
	csv_file.close()
	
	# get the column numbers for the headers
	csv_header_column_numbers = get_variable_column_numbers(open(path_to_csv_file, 'r'), 0)
	excel_header_column_numbers = get_variable_column_numbers(excel_worksheet, excel_header_row_number)
	
	# list of data to be entered into the csv file row
	row_insert = []
	
	for variable in report.variables:
				
		# get the column number and variable name mapping for the csv file
		csv_col_num = csv_header_column_numbers[variable.name]
				
		for row_num in range(excel_worksheet.nrows):
			print("row num: " + str(row_num))
			if row_num > excel_header_row_number:
				print("Row num greater than header row num")
				cell_value = None
				
				print("var is composite: " + str(variable.is_composite))
				
				# basic variable
				if not variable.is_composite:
					
					# since this is a basic variable, the header names in the Excel and CSV
					# will match, so get the Excel variable column number
					excel_col_num = excel_header_column_numbers[variable.name]
					
					print("Excel col num: " + str(excel_col_num))
			
					cell_value = cleanup_excel_data(variable, cell_value, excel_workbook_datemode)
					
				# composite variable
				else:
					if variable.data_type == "date":
						old_date_variable_name = variable.variables_composite_made_of[0]
						new_date_variable_name = variable.variables_composite_made_of[1]
						
						old_date_variable_column_num = excel_header_column_numbers[old_date_variable_name]
						new_date_variable_column_num = excel_header_column_numbers[new_date_variable_name]
						
						old_date = excel_worksheet.cell(row_num, old_date_variable_column_num).value
						new_date = excel_worksheet.cell(row_num, new_date_variable_column_num).value
						
						# cleanup the dates before computing the difference
						old_date = cleanup_excel_data(variable, old_date, excel_workbook_datemode)
						new_date = cleanup_excel_data(variable, new_date, excel_workbook_datemode)
						
						if variable.composite_method == 'date_diff_days':
							cell_value = date_diff_days(old_date, new_date)
							
				# insert the cell value
				row_insert.append(cell_value)

		print("Row: " + str(row_insert))
		# write the row
		csv_writer.writerow(row_insert)
			
	# close the file
	csv_file.close()
	
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
		csv_reader = csv.reader(spreadsheet)
		
		for row in csv_reader:
			
			if current_row == header_row_num:
				column_number = 0
				for header_name in row:
					print("CSV header name: " + header_name)
					header_name_column_number[header_name] = column_number
					column_number = column_number + 1
				break
				
			else:
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