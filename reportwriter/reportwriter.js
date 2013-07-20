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
	json_string = JSON.stringify(json_data, null, '\t');
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
		
		/** name **/
		var variable_name = document.getElementById(variable_id + "_name").innerHTML;
		report_data["variables"][variable_name] = {};
		
		/** data type **/
		var data_type = document.getElementById(variable_id + "_data_type");
		data_type_value = data_type.options[data_type.selectedIndex].text;
		report_data["variables"][variable_name]["data_type"] = data_type_value;
		
		/** is_transform **/
		var is_transform = document.getElementById(variable_id + "_is_transform");
		is_transform_value = is_transform.options[is_transform.selectedIndex].text;
		
		var is_transform_bool = false;
		if (is_transform_value=="true") {
			is_transform_bool = true;
		}
		report_data["variables"][variable_name]["is_transform"] = is_transform_bool;
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
	
	var variable_id = variable_name.replace(/\W/g);
	
	/**Create a new container for this variable**/
	var variable = document.createElement('div');
	variable.setAttribute('class','variable')
	variable.setAttribute('id', variable_id)
	
	/** variable name **/
	var variable_name_display = document.createElement('h2');
	variable_name_display.setAttribute('id', variable_id + "_name")
	variable_name_display.innerHTML = variable_name;
	variable.appendChild(variable_name_display)
	
	/** data type **/
	var data_type_label = document.createElement('label')
	data_type_label.innerHTML = "Data type";
	variable.appendChild(data_type_label);
	
	var data_type = document.createElement('select');
	data_type.setAttribute('id', variable_id + "_data_type")

		/** int **/
		data_type_int = document.createElement('option');
		data_type_int.innerHTML = "Integer";
		data_type.appendChild(data_type_int);
		
		/** float **/
		data_type_float = document.createElement('option');
		data_type_float.innerHTML = "Float";
		data_type.appendChild(data_type_float);
		
		/** date **/
		data_type_date = document.createElement('option');
		data_type_date.innerHTML = "Date";
		data_type.appendChild(data_type_date);
		
		/** boolean **/
		data_type_boolean = document.createElement('option');
		data_type_boolean.innerHTML = "Boolean";
		data_type.appendChild(data_type_boolean);
		
		/** string **/
		data_type_string = document.createElement('option');
		data_type_string.innerHTML = "String";
		data_type.appendChild(data_type_string);
	
	variable.appendChild(data_type);
	
	/** is transform **/
	
	var is_transform_label = document.createElement('label')
	is_transform_label.innerHTML = "Transform this variable";
	variable.appendChild(is_transform_label);
	
	var is_transform = document.createElement('select');
	is_transform.setAttribute('id', variable_id + "_is_transform")
	is_transform.setAttribute('onchange', 'toggle_transform_options(this.options[this.selectedIndex].value,"' + variable_id + '")');

		/** false **/
		is_transform_false = document.createElement('option');
		is_transform_false.innerHTML = "false";
		is_transform.appendChild(is_transform_false);
		
		/** true **/
		is_transform_true = document.createElement('option');
		is_transform_true.innerHTML = "true";
		is_transform.appendChild(is_transform_true);
		
	variable.appendChild(is_transform);
	
	/** remove variable **/
	var remove_variable = document.createElement('div');
	remove_variable.setAttribute('onclick','remove_variable("' + variable_id + '")');
	remove_variable.setAttribute('class','clickable');
	remove_variable.innerHTML = "[Remove]";
	variable.appendChild(remove_variable);
	
	/** Add the variable to the variables container **/
	variables_container.appendChild(variable);
}

function toggle_transform_options(is_transform, variable_id){

	/** variable dom element **/
	var variable = document.getElementById(variable_id);
	
	if (is_transform == "true"){
		set_transform_options(variable_id)
	}
	else{
		var transform_options_id = variable_id + "_transform_options";
		var transform_options = document.getElementById(transform_options_id);
		variable.removeChild(transform_options);
	}
}

function set_transform_options(variable_id){
	/** update the variables before starting **/
	update_variables();
	
	/** variable dom element **/
	var variable = document.getElementById(variable_id);
	/** variable options registered with the report_data **/
	var report_variables = report_data["variables"];
	
	/** transform options **/
	transform_options = document.createElement('div');
	transform_options.setAttribute('id', variable_id + "_transform_options");
	transform_options.setAttribute('class', "transform_options");
	variable.appendChild(transform_options);
	
	/** variable container **/
	variable_checkbox_container = document.createElement('div');
	transform_options.appendChild(variable_checkbox_container);
	
	for (var report_variable_name in report_variables) {
		var report_variable = report_variables[report_variable_name];
		var is_transform = report_variable['is_transform'];
		if(!is_transform){
			/**non-transformed variable, so add it as a selectable option**/
			
			
			variable_checkbox_name = document.createElement('span');
			variable_checkbox_name.innerHTML = report_variable_name;
			
			variable_checkbox_container.appendChild(variable_checkbox_name);
			
			variable_checkbox = document.createElement('input');
			variable_checkbox.setAttribute('type','checkbox');
			variable_checkbox.setAttribute('value','checkbox');
			variable_checkbox.checked = false;
			variable_checkbox_container.appendChild(variable_checkbox);
			
			/**TODO: check if this option has been selected already**/
		}
	}
	
	/** the method to use **/
	//var method_label = document.createElement('label')
	//method.innerHTML = "Method (not implemented)";
	//variable.appendChild(method_label);

	
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