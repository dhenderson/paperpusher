import sys
sys.path.append('../')

import json_helper
import spreadsheet_helper
import csv
import xlrd
from models import Report, BasicVariable, TransformVariable, ExcelWorksheetContainer, CsvFileContainer


def get_test_report():
	# load the report
	report = json_helper.load_report_from_json('test_files/test.json')
	# add additional header values
	report.additional_header_names = ["Is test?"]
	
	return report

def get_test_excel_worksheet_container():
	workbook = xlrd.open_workbook('test_files/test.xlsx')
	datemode = workbook.datemode
	worksheet = workbook.sheet_by_index(0)
	header_row_number = 1
	
	excel_worksheet_container = ExcelWorksheetContainer(worksheet, datemode, header_row_number)
	
	return excel_worksheet_container
	
def test_excel_worksheet_to_csv():

	report = get_test_report()
	path_to_csv_output = "test_files/test_excel_to_csv.csv"
	excel_worksheet_container = get_test_excel_worksheet_container()
	
	excel_header_row_number = excel_worksheet_container.header_row_number
	excel_worksheet = excel_worksheet_container.worksheet
	datemode = excel_worksheet_container.datemode
		
	spreadsheet_helper.excel_worksheet_to_csv(excel_worksheet, excel_header_row_number, datemode, path_to_csv_output, report.variables)
	
	print("test_excel_worksheet_to_csv()")
	
def test_generate_master_csv():
	
	report = get_test_report()
	path_to_master_csv_file = 'test_files/test_master.csv'
	report.path_to_master_csv_file = path_to_master_csv_file
	
	csv_file_container = CsvFileContainer("test_files/test_excel_to_csv.csv", ["True"])
	
	spreadsheet_helper.generate_master_csv(path_to_master_csv_file, report, [csv_file_container])
	
	print("##test_generate_master_csv##")
	print("generated " + path_to_master_csv_file)
	
if __name__ == "__main__":
	test_excel_worksheet_to_csv()
	test_generate_master_csv()