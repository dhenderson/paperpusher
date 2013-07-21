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
	var remove_variable = document.createElement('span');
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
	
	// transform method
	add_transform_method(variable_id)
	
	// add an initiatal transform variable option
	add_transform_variable_options(report_variables, variable_id); 	
	
	// button to add another transform variable
	var add_another_transform_variable_button = document.createElement('span');
	add_another_transform_variable_button.setAttribute('class', "clickable");
	add_another_transform_variable_button.setAttribute('onclick', 'add_transform_variable_options(report_data["variables"], "' + variable_id + '")');
	add_another_transform_variable_button.innerHTML = "Add another variable";
	transform_options.appendChild(add_another_transform_variable_button);
	
	/** the method to use **/
	//var method_label = document.createElement('label')
	//method.innerHTML = "Method (not implemented)";
	//variable.appendChild(method_label);
}

function add_transform_variable_options(report_variables, variable_id) {

	var transform_variable_options_container = document.createElement('div');
	var transform_variable_options = document.createElement('select');
	var transform_container_id = variable_id + "_transform_options";
	var transform_container = document.getElementById(transform_container_id);
	var transform_variable_label = document.createElement('label');
	
	transform_variable_label.innerHTML = "Transform variables";
	transform_variable_options_container.appendChild(transform_variable_label);
	
	for (var report_variable_name in report_variables) {
		var report_variable = report_variables[report_variable_name];
		var is_transform = report_variable['is_transform'];
		if(!is_transform){
			/**non-transformed variable, so add it as a selectable option**/
			var transform_option = document.createElement('option');
			transform_option.innerHTML = report_variable_name;
			transform_variable_options.appendChild(transform_option);
			
			/**TODO: check if this option has been selected already**/
		}
	}
	transform_variable_options_container.appendChild(transform_variable_options);
	transform_container.appendChild(transform_variable_options_container);
		
	// add it to the transform container
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

function add_transform_method(variable_id) {
	var transform_container = document.getElementById(variable_id + "_transform_options");
	var transform_method_container = document.createElement('div');
	var transform_method = document.createElement('select');
	var transform_method_label = document.createElement('label');
	
	transform_method_label.innerHTML = "Transform method";
	
	// date_diff_days
	var date_diff_days = document.createElement('option');
	date_diff_days.innerHTML = "date_diff_days";
	transform_method.appendChild(date_diff_days);
	
	// begins_with
	var begins_with = document.createElement('option');
	begins_with.innerHTML = "begins_with";
	transform_method.appendChild(begins_with);
	
	// not_null
	var not_null = document.createElement('option');
	not_null.innerHTML = "not_null";
	transform_method.appendChild(not_null);
	
	// append
	transform_method_container.appendChild(transform_method_label);
	transform_method_container.appendChild(transform_method);
	transform_container.appendChild(transform_method_container);
}


