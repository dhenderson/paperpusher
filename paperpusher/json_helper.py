import json
from paperpusher.report import Report, SummarySection, Objective, Chart
from paperpusher.variable import BasicVariable, TransformVariable, SummaryVariable, Group


# value for the all observations group
group_all_observations = "All observations"

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
		
	# groups
	if 'groups' in json_data:
		for group_name in json_data['groups']:
			variable_name = json_data['groups'][group_name]['variable']
			variable_must_be = json_data['groups'][group_name]['variable_must_be']
			variable_values = json_data['groups'][group_name]['variable_values']
			group = Group(group_name, variable_name, variable_must_be, variable_values)
			report.groups[group_name] = group
		
	# summary sections
	for summary_section_name in json_data['summary_sections']:
		summary_section = SummarySection(summary_section_name)
		
		# summary variables
		for summary_variable_name in json_data['summary_sections'][summary_section_name]['summary_variables']:
			
			summary_variable = SummaryVariable(summary_variable_name, 
					json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['variables'], 
					json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['methods'])
										
			# attach groups to summary variables
			if 'groups' in json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]:
				for group_name in json_data['summary_sections'][summary_section_name]['summary_variables'][summary_variable_name]['groups']:
					if group_name == 'group_all_observations':
						group = create_all_group()
					else:
						group = report.groups[group_name]
					
					# add to the report and summary variable gropus
					if group_name not in report.groups:
						report.groups[group.name] = group					
					summary_variable.groups.append(group)
			else:
				# no group specified, so create an "all" group
				group = create_all_group()
				if group.name not in report.groups:
					report.groups[group.name] = group					
				summary_variable.groups.append(group)
					
			summary_section.summary_variables[summary_variable_name] = summary_variable
			
		report.summary_sections.append(summary_section)
		
		# objectives
		if 'objectives' in json_data['summary_sections'][summary_section_name]:
			for objective_name in json_data['summary_sections'][summary_section_name]['objectives']:
				
				if 'group' not in json_data['summary_sections'][summary_section_name]['objectives'][objective_name]:
					group_name = group_all_observations
					
				if group_name == group_all_observations:
					group = create_all_group()
				else:
					group = report.groups[group_name]
				
				summary_variable_name = json_data['summary_sections'][summary_section_name]['objectives'][objective_name]['summary_variable']
				summary_variable = summary_section.summary_variables[summary_variable_name]
				method = json_data['summary_sections'][summary_section_name]['objectives'][objective_name]['method']
				objective_values = json_data['summary_sections'][summary_section_name]['objectives'][objective_name]['objective_values']
				objective_must_be = json_data['summary_sections'][summary_section_name]['objectives'][objective_name]['objective_must_be']
				
				objective = Objective(objective_name, method, summary_variable, objective_must_be, objective_values, group)
				
				summary_section.objectives.append(objective)
			
		# charts
		if 'charts' in json_data['summary_sections'][summary_section_name]:
			for chart_name in json_data['summary_sections'][summary_section_name]['charts']:
			
				# get the summary variable for this chart
				for summary_variable_name in summary_section.summary_variables:
					if summary_variable_name == json_data['summary_sections'][summary_section_name]['charts'][chart_name]['summary_variable']:
						summary_variable = summary_section.summary_variables[summary_variable_name]
						break
						
				method = json_data['summary_sections'][summary_section_name]['charts'][chart_name]['method']
				type = json_data['summary_sections'][summary_section_name]['charts'][chart_name]['type']
				group_names = []
				
				for group_name in json_data['summary_sections'][summary_section_name]['charts'][chart_name]['groups']:
					group_names.append(group_name)
					
				chart = Chart(chart_name, summary_variable, method, type, group_names)
				
				summary_section.charts.append(chart)
				

	return report
	
def create_all_group():
	name = group_all_observations
	variable_name = None
	variable_must_be = None
	variable_values = None
	group = Group(name, variable_name, variable_must_be, variable_values, False)
			
	return group
	
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
			
	json_data['summary_sections'] = {}
	for summary_section in report.summary_sections:
		json_data['summary_sections'][summary_section.name] =  {}
		json_data['summary_sections'][summary_section.name]['summary_variables'] =  {}
		
		for summary_variable_name in summary_section.summary_variables:
			summary_variable = summary_section.summary_variables[summary_variable_name]
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name] = {}
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['variables'] = summary_variable.variables
			json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['methods'] = summary_variable.methods
			# TODO: save groups
			# TODO: save objectives
			#json_data['summary_sections'][summary_section.name]['summary_variables'][summary_variable.name]['groups'] = summary_variable.groups
			
	
			
	save_json(path_to_json_file, json_data)