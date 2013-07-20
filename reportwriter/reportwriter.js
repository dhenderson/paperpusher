var report_data = {"name" : "New report"}

/**
* Loads a Paper Pusher report json file.
* @param {string} path_to_report_file Path to a Paper Pusher json file
* @return returns a javascript map of a Paper Pusher report
**/
function load_report_json_file(path_to_report_file){
	return JSON.parse(readJSON(path_to_report_file));
}

/**
* Downloads a .json file representing a Paper Pusher report
* data structure
* @param {map} json_data a Paper Pusher map structure
* @param {string} report_file_name the name of the report file to be downloaded
**/
function save_report_json_file(json_data, report_file_name){

	/**update the report data before saving**/
	update_report_properties();
	update_variables();
	
	/** convert the report_data into a json string and download the file**/
	json_string = JSON.stringify(json_data);
	report_file_name = report_file_name + ".json";
	var blob = new Blob([json_string], {type: "text/plain;charset=utf-8"});
	saveAs(blob, report_file_name);
}

/**
* Updates the report_data Paper Pusher report elements for 
* items in the "Report properties" section
**/
function update_report_properties(){
	var report_name = document.getElementById('report_name').value;
	var report_description = document.getElementById('report_description').value;
	report_data["name"] = report_name;
	report_data["description"] = report_description;
}

function update_variables(){
	var variables = document.getElementById('variables');
	report_data["variables"] = {}

	/** get each variable **/
	
	var variables = document.getElementById('variables').childNodes;
	for(i=0; i< variables.length; i++) {
		var variable = variables[i];
		
		var variable_id = variable.id;
		var variable_name = document.getElementById(variable_id + "_name").innerHTML;
		report_data["variables"][variable_name] = {}
	}
}

/**
* Converts a string of variable names separated by line breaks into
* report variables
**/
function add_variables_by_string(variable_names_str) {
	var variable_names = variable_names_str.split("\n");
	
	/**Create a new variable for each variable name**/
	for (var i = 0; i < variable_names.length; i++) {
		variable_name = variable_names[i]
		/**Remove trailing characters**/
		variable_name.replace(/^\s+|\s+$/g, '')
		if (variable_name != "") {
			add_variable(variable_name)
		}
	}
	
	/**The variables have been added, so clear the varible names textbox**/
	document.getElementById('add_variables').value = "";
}

/**
* Adds a new report variable
* @param {string} variable_name
**/
function add_variable(variable_name){
	var variables_container = document.getElementById('variables');
	
	var variable_id = 'variable_' + variable_name.replace(/\W/g, '');
	
	/**Create a new container for this variable**/
	var variable = document.createElement('div');
	variable.setAttribute('class','variable')
	variable.setAttribute('id', variable_id)
	
	/** variable name **/
	var variable_name_div = document.createElement('div');
	variable_name_div.setAttribute('id', variable_id + "_name")
	variable_name_div.innerHTML = variable_name;
	variable.appendChild(variable_name_div)
	
	/** remove variable **/
	var remove_variable = document.createElement('span')
	remove_variable.setAttribute('onclick','remove_variable("' + variable_id + '")')
	remove_variable.setAttribute('class','clickable')
	remove_variable.innerHTML = " [Remove] "
	variable.appendChild(remove_variable)
	
	/** Add the variable to the variables container **/
	variables_container.appendChild(variable)
}

/**
* Removes a variable by a given id
* @param {string} variable_id
**/
function remove_variable(variable_id){
	var variable = document.getElementById(variable_id)
	var variables_container = document.getElementById('variables');
	variables_container.removeChild(variable)
}