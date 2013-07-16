import json

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