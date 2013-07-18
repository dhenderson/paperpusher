import sys
sys.path.append('../')
import json_helper
import spreadsheet_helper
import csv
import xlrd
from models import Report, BasicVariable, TransformVariable, ExcelWorkbookContainer

def test_generate_csv_file_from_excel_worksheets():

	# excel workbook
	excel_workbook_containers = []
	
	workbook = xlrd.open_workbook('test.xlsx')
	excel_workbook_container = ExcelWorkbookContainer('test.xlsx', workbook)
	excel_workbook_container.worksheet_index_header_row_num[0] = 1
	excel_workbook_container.additional_cell_values.append("True")
	
	excel_workbook_containers.append(excel_workbook_container)
	
	# load the report
	report = json_helper.load_report_from_json('test.json')
	# add additional header values
	report.additional_header_names = ["Is test?"]
	
	# csv file path
	path_to_csv_file = 'test.csv'
	
	spreadsheet_helper.generate_csv_file_from_excel_worksheets(path_to_csv_file, report, excel_workbook_containers)
	
if __name__ == "__main__":
	test_generate_csv_file_from_excel_worksheets()