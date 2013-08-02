function ReportController($scope) {
	
	// report properties
	$scope.report_name = null;
	$scope.description = null;
	$scope.variables = {};
	$scope.groups = {};
	$scope.summarySections = {}
	
	$scope.dataTypeOptions = [
				{dataType : 'int', display_value : 'Integer'},       
				{dataType : 'float', display_value : 'Float'},
				{dataType : 'string', display_value : 'Text'},
				{dataType : 'boolean', display_value : 'Boolean'},
				{dataType : 'date', display_value : 'Date'}
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
					dataType: 'int'
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
	
	$scope.addSummaryVariable = function(newSummaryVariableName, summarySectionName) {
	
		$scope.summarySections[summarySectionName]['summary_variables'][newSummaryVariableName] = {
			name : newSummaryVariableName,
			variables : [],
			methods : [],
			groups : []
		};
		
		newSummaryVariableName = null;
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