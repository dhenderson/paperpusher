import test_spreadsheet

def test_generate_report():

	report = test_spreadsheet.get_test_report()
	report.generate_report()
	
if __name__ == "__main__":
	test_generate_report()