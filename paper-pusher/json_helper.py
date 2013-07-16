import json
from model import *

# Loads the json file at the specified path and returns 
# the json data model as python lists and dictionaries
def load_json(path_to_json_file):
	json_file = open(path_to_json_file)
	json_data = json.load(json_file)
	json_file.close()
	
	return json_data
	
# Saves the data model in the from of list or dictionary into json at
# the specificed json file location
def save_json(path_to_json_file, data):
	try:
		# open the json file
		json_file = open(path_to_json_file, 'w')
		
		# convert the python list or dictionary into json
		data_string = json.dumps(data, sort_keys=True, indent=4)
		
		# write and close the file
		json_file.write(data_string)
		json_file.close()
		
		return True
	
	except:
		return False
		
def load_report_from_json(path_to_json_file):
	json_data = load_json(path_to_json_file)
	report_name = json_data['name']
	
	report = Report(report_name)
	
	for variable_name in json_data['variables']:
	
		# unpack the variable attributes that are 
		# common for BasicVariable and CompositeVariable classes
		is_composite = json_data['variables'][variable_name]['is_composite']
		data_type = json_data['variables'][variable_name]['data_type']
		
		variable = None
		
		if not is_composite:
			variable = BasicVariable(variable_name, data_type)
		else:
			variable = CompositeVariable(variable_name, data_type)
			variable.variables = json_data['variables'][variable_name]['composite_definition']['variables']
			variable.composite_method = json_data['variables'][variable_name]['composite_definition']['composite_method']
		
		report.variables.append(variable)
		
	return report
			