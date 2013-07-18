import sys
sys.path.append('../')
import json_helper

def test_save_report_as_json():
	path_to_csv_file = 'test2.json'
	# load the report
	report = json_helper.load_report_from_json('test.json')
	
	json_helper.save_report_as_json(path_to_csv_file, report)
	
if __name__ == "__main__":
	test_save_report_as_json()