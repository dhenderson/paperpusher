import config
import spreadsheet
import csv
import xlrd
from report import Report, BasicVariable, CompositeVariable

# open the test json file
data = config.load_json('test.json')

# save the data in the test json file
config.save_json('test.json', data)

def test_append_excel_worksheet_to_csv():

	# excel workbook
	workbook = xlrd.open_workbook('test.xlsx')
	worksheet = workbook.sheet_by_index(0)
	excel_header_row_number = 1
	
	# csv file
	path_to_csv_file = 'test.csv'
	
	# define a report
	report = Report("Test report")
	
	# variables
	first_name = BasicVariable("First name", "string")
	date_of_birth = BasicVariable("Date of birth", "date")
	
	# add variables to the report
	report.variables.append(first_name)
	report.variables.append(date_of_birth)
	
	spreadsheet.append_excel_worksheet_to_csv(worksheet, workbook.datemode, path_to_csv_file, report, excel_header_row_number)
	
if __name__ == "__main__":
	test_append_excel_worksheet_to_csv()