import sys
sys.path.append('../')

import json_helper
import spreadsheet_helper
import csv
import xlrd
from models import Report, BasicVariable, TransformVariable, ExcelWorkbookContainer

def get_test_excel_workbook_container():
	workbook = xlrd.open_workbook('test.xlsx')
	excel_workbook_container = ExcelWorkbookContainer('test.xlsx', workbook)
	excel_workbook_container.worksheet_index_header_row_num[0] = 1
	
	return excel_workbook_container

def test_generate_csv_file_from_excel_worksheets():

	# excel workbook
	excel_workbook_containers = []
	
	excel_workbook_container = get_test_excel_workbook_container()
	excel_workbook_containers.append(excel_workbook_container)
	
	# load the report
	report = json_helper.load_report_from_json('test.json')
	# add additional header values
	report.additional_header_names = ["Is test?"]
	
	# csv file path
	path_to_csv_file = 'test.csv'
	
	spreadsheet_helper.generate_csv_file_from_excel_worksheets(path_to_csv_file, report, excel_workbook_containers)
	
def test_excel_worksheet_to_csv():

	path_to_csv_output = "test_excel_to_csv.csv"
	excel_workbook_container = get_test_excel_workbook_container()
	for worksheet_index in excel_workbook_container.worksheet_index_header_row_num:
	
		excel_header_row_num = excel_workbook_container.worksheet_index_header_row_num[worksheet_index]
		excel_worksheet = excel_workbook_container.workbook.sheet_by_index(worksheet_index)
		
		spreadsheet_helper.excel_worksheet_to_csv(excel_worksheet, excel_header_row_num, path_to_csv_output)
		
		print("test_excel_worksheet_to_csv()")
		
		break
	
if __name__ == "__main__":
	test_generate_csv_file_from_excel_worksheets()
	test_excel_worksheet_to_csv()