import test_spreadsheet_helper

def test_generate_report():

	report = test_spreadsheet_helper.get_test_report()
	report.generate_report()
	
if __name__ == "__main__":
	test_generate_report()