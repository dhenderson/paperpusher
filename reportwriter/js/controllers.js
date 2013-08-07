function ReportController($scope) {
	
	// report properties
	$scope.report_name = null;
	$scope.description = null;
	$scope.variables = {};
	$scope.groups = {};
	$scope.summarySections = {};
	
	$scope.data_typeOptions = [
				{data_type : 'int', display_value : 'Integer'},       
				{data_type : 'float', display_value : 'Float'},
				{data_type : 'string', display_value : 'Text'},
				{data_type : 'boolean', display_value : 'Boolean'},
				{data_type : 'date', display_value : 'Date'}
			];
			
	$scope.transform_methodOptions = [
			{transform_method : 'date_diff_days', display_value : 'Date difference in days'}, 
			{transform_method : 'begins_with', display_value : 'Begins with'}, 
			{transform_method : 'not_empty', display_value : 'Not empty'}
		];
		
	$scope.must_be_options = [
		{must_be: 'equal', display_value : 'Equal to'},
		{must_be: 'greater_than_equal_to', display_value : 'Greater than equal to'},
		{must_be: 'less_than', display_value : 'Less than'},
		{must_be: 'between', display_value : 'Between'},
		{must_be: 'in', display_value : 'In given values'},
		{must_be: 'not_in', display_value : 'Not in given values'}
	];
	
	$scope.summaryMethodOptions = [
		{method: 'min', display_value : 'Min'},
		{method: 'max', display_value : 'Max'},
		{method: 'mean', display_value : 'Average'},
		{method: 'median', display_value : 'Median'},
		{method: 'sum', display_value : 'Sum'},
		{method: 'percent_of_obs', display_value : 'Percent of observations'},
		{method: 'percent_of_sum', display_value : 'Percent of sum (var 1/var 2)'},
		{method: 'percent_of_average', display_value : 'Percent of average (var 1/var 2)'},
	];
	
	/**
	* Creates a new variable
	**/
	$scope.addVariable = function() {
		if(typeof $scope.variables[$scope.newVariableName] == 'undefined') {
				$scope.variables[$scope.newVariableName] = { 
					name: $scope.newVariableName, 
					isTransform : false, 
					data_type: 'int'
				};
				$scope.newVariableName = null;
			}
		}
	
	/**
	* Removes a variable by name, where each variable name is assumed unique
	**/
	$scope.removeVariable = function(variableName) {
		delete $scope.variables[variableName];
	}
	
	/**
	* Adds a TransformVariable
	**/
	$scope.addTransformVariable = function() {
		if(typeof $scope.variables[$scope.newTransformVariableName] == 'undefined') {
			$scope.variables[$scope.newTransformVariableName] = { 
				name: $scope.newTransformVariableName, 
				is_transform : true, 
				data_type: 'int', 
				transform_definition : {
					transform_method : "not_empty",
					variables : [],
					arguments : []
				}
			};
			
			$scope.newTransformVariableName = null;
		}
	}
	
	$scope.addGroup = function() {
		$scope.groups[$scope.newGroupName] = {
			name : $scope.newGroupName,
			variable : null,
			variable_must_be : 'equal',
			variable_values : []
		}
		$scope.newGroupName = null;
	}
	
	$scope.removeGroup = function(groupName) {
		delete $scope.groups[groupName];
	}

	$scope.addSummarySection = function() {
		$scope.summarySections[$scope.newSummarySectionName] = {
			name : $scope.newSummarySectionName,
			summary_variables : {}
		}
		$scope.newSummarySectionName = null;
	}
	$scope.removeSummarySection = function(summarySectionName) {
		delete $scope.summarySections[summarySectionName];
	}
	
	/**
	* Adds a new summary variable
	**/
	$scope.addSummaryVariable = function(newSummaryVariableName, summarySectionName) {
	
		$scope.summarySections[summarySectionName]['summary_variables'][newSummaryVariableName] = {
			name : newSummaryVariableName,
			variables : [],
			methods : [],
			groups : []
		};
		
		newSummaryVariableName = null;
	}
	
	/**
	* If the method for a summary variable is in the methods list, remove it 
	* and set the checkbox to unchecked. Otherwise, set the checkbox to 
	* checked and add the method to the methods list.
	**/
	$scope.toggle_summary_variable_method = function(method_name, summary_section_name, summary_variable_name, checkbox) {
		var methods = $scope.summarySections[summary_section_name]['summary_variables'][summary_variable_name]['methods'];
		
		var method_in_list = false;
		for (var i=methods.length-1; i>=0; i--) {
			if (methods[i] === method_name) {
				methods.splice(i, 1);
				method_in_list = true;
			}
		}
		if (method_in_list) {
			checkbox.checked=false;
		}
		else {
			methods.push(method_name)
			checkbox.checked=true;
		}
	}
	
	$scope.toggle_summary_variable_group = function(group_name, summary_section_name, summary_variable_name, checkbox) {
		
		// add 'groups' if it's not in there
		if ('groups' in $scope.summarySections[summary_section_name]['summary_variables'][summary_variable_name]) {}
		else{
			$scope.summarySections[summary_section_name]['summary_variables'][summary_variable_name]['groups'] = [];
		}
		
		var groups = $scope.summarySections[summary_section_name]['summary_variables'][summary_variable_name]['groups'];
		
		var group_in_list = false;
		for (var i=groups.length-1; i>=0; i--) {
			if (groups[i] === group_name) {
				groups.splice(i, 1);
				group_in_list = true;
			}
		}
		if (group_in_list) {
			checkbox.checked=false;
		}
		else {
			groups.push(group_name)
			checkbox.checked=true;
		}
		
		alert(groups);
	}
	
	/**
	* Returns true if the passed value is in the array. Otherwise returns false.
	**/
	$scope.is_value_in_array = function(value, array){
		try {
			for (var i=array.length-1; i>=0; i--) {
				if (array[i] === value) {
					return true;
				}
			}
		}
		catch(err){return false}
		return false;
	}
	
	/**
	* Adds a new objective
	**/
	$scope.addObjective = function(newObjectiveName, summarySectionName) {
		$scope.summarySections[summarySectionName]['objectives'][newObjectiveName] = {
			name : newObjectiveName,
			group : null,
			method : null,
			objective_values : [],
			objective_must_be : null,
			summary_variable : null
		};
		newObjectiveName = null;
	}
	
	$scope.removeObjective = function(objectiveName, summarySectionName) {
		delete $scope.summarySections[summarySectionName]['objectives'][objectiveName];
	}
	
	// upload a paper pusher report recipe json file
	set_uploaded_json_file_contents = function(contents){
		$scope.$apply(function() {
			var uploaded_json_file = $.parseJSON(contents);
			$scope.formReportName = uploaded_json_file.name;
			$scope.formDescriptionText = uploaded_json_file.description;
			$scope.variables = uploaded_json_file.variables;
			$scope.groups = uploaded_json_file.groups;
			$scope.summarySections = uploaded_json_file.summary_sections;
		});
	}
	
	$scope.save = function() {
		// set the basic properties
		$scope.reportName = $scope.formReportName;
		$scope.description = $scope.formDescriptionText;
		
		jsonData = {
			"name" : $scope.reportName, 
			"description" : $scope.description,
			"variables" : $scope.variables,
			"groups" : $scope.groups,
			"summary_sections" : $scope.summarySections,
		};
		
		// download the json file
		jsonDownload = angular.toJson(jsonData, pretty=true);
		
		window.location.href = "data:text;base64," + jsonDownload;
		document.location = 'data:Application/octet-stream,' + encodeURIComponent(jsonDownload);
	};
}