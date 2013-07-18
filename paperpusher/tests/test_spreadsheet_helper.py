import sys
sys.path.append('../')

import json_helper
import spreadsheet_helper
import csv
import xlrd
from models import Report, BasicVariable, TransformVariable, ExcelWorksheetContainer


def get_test_report():
	# load the report
	report = json_helper.load_report_from_json('test.json')
	# add additional header values
	report.additional_header_names = ["Is test?"]
	
	return report

def get_test_excel_worksheet_container():
	workbook = xlrd.open_workbook('test.xlsx')
	datemode = workbook.datemode
	worksheet = workbook.sheet_by_index(0)
	header_row_number = 1
	
	excel_worksheet_container = ExcelWorksheetContainer(worksheet, datemode, header_row_number)
	
	return excel_worksheet_container
	
def test_excel_worksheet_to_csv():

	report = get_test_report()
	path_to_csv_output = "test_excel_to_csv.csv"
	excel_worksheet_container = get_test_excel_worksheet_container()
	
	excel_header_row_number = excel_worksheet_container.header_row_number
	excel_worksheet = excel_worksheet_container.worksheet
	datemode = excel_worksheet_container.datemode
		
	spreadsheet_helper.excel_worksheet_to_csv(excel_worksheet, excel_header_row_number, datemode, path_to_csv_output, report.variables)
	
	print("test_excel_worksheet_to_csv()")
	
if __name__ == "__main__":
	test_excel_worksheet_to_csv()