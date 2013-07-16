import config
import spreadsheet
import csv
import xlrd

# open the test json file
data = config.load_json('test.json')

# save the data in the test json file
config.save_json('test.json', data)

def test_append_excel_worksheet_to_csv():

	workbook = xlrd.open_workbook('test.xlsx')
	worksheet = workbook.sheet_by_index(0)
	excel_header_row_number = 1
	write_header = True
	
	csv_file = open('test.csv')
	variable_definitions = config.load_json('test.json')
	
	spreadsheet.append_excel_worksheet_to_csv(worksheet, workbook.datemode, csv_file, variable_definitions, excel_header_row_number, write_header)
	
if __name__ == "__main__":
	test_append_excel_worksheet_to_csv()