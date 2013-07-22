import json
from paperpusher.report import Report, SummarySection
from paperpusher.variable import BasicVariable, TransformVariable, SummaryVariable

# Loads the json file at the specified path and returns 
# the json data model as python lists and dictionaries
def load_json(path_to_json_file):
	json_file = open(path_to_json_file)
	json_data = json.load(json_file)
	json_file.close()
	
	return json_data
	
# Saves the data model in the form of list or dictionary into json at
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
		# common for BasicVariable and TransformVariable classes
		is_transform = json_data['variables'][variable_name]['is_transform']
		data_type = json_data['variables'][variable_name]['data_type']
		
		variable = None
		
		if not is_transform:
			variable = BasicVariable(variable_name, data_type)
		else:
			variable = TransformVariable(variable_name, data_type)
			variable.variables = json_data['variables'][variable_name]['transform_definition']['variables']
			variable.transform_method = json_data['variables'][variable_name]['transform_definition']['transform_method']
			
			# if arguments are passed for the transform method, get them
			if 'arguments' in json_data['variables'][variable_name]['transform_definition']:
				variable.arguments = json_data['variables'][variable_name]['transform_definition']['arguments']
		
		report.variables.append(variable)
		
	for summary_section_name in json_data['summary_sections']:
		summary_section = SummarySection(summary_section_name)
		
		for summary_variable_name in json_data['summary_sections'][summary_section_name]['summary_variables']:
			
			summary_variable = SummaryVariable(summary_variable_name, 
					json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['variables'], 
					json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['methods'])
										
			if 'where' in json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]:
				summary_variable.where = json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['where']
					
			summary_section.summary_variables.append(summary_variable)
			
		report.summary_sections.append(summary_section)

	return report
	
def save_report_as_json(path_to_json_file, report):
	# setup the basic json data structure
	json_data = {"name" : report.name, "description" : report.description, "variables" : {}}
	
	for variable in report.variables:
		json_data['variables'][variable.name] = {"data_type" : variable.data_type, "is_transform" : variable.is_transform}
		
		if variable.is_transform:
			json_data['variables'][variable.name]["transform_definition"] =  {}
			json_data['variables'][variable.name]["transform_definition"]["transform_method"] = variable.transform_method
			json_data['variables'][variable.name]["transform_definition"]["variables"] = variable.variables
			json_data['variables'][variable.name]["transform_definition"]["arguments"] = variable.arguments
			
	for summary_section in report.summary_sections:
		json_data['summary_sections'][summary_section.name] =  {}
		json_data['summary_sections'][summary_section.name]['summary_variables'] =  {}
		
		for summary_variable in summary_section.variables:
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name] = {}
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['variables'] = summary_variable.variables
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['methods'] = summary_variable.methods
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['where'] = summary_variable.where
			
	save_json(path_to_json_file, json_data)