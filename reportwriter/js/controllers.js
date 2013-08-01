function ReportController($scope) {
	
	// report properties
	$scope.report_name = null;
	$scope.description = null;
	$scope.variables = {};
	$scope.groups = {};
	$scope.summarySections = {}
	
	$scope.isTransformOptions = [
				{isTransform : false, displayValue : 'Use this variable as is' },       
				{isTransform : true, displayValue : 'Transform this variable' }
			];
	$scope.dataTypeOptions = [
				{dataType : 'int', displayValue : 'Integer'},       
				{dataType : 'float', displayValue : 'Float'},
				{dataType : 'string', displayValue : 'Text'},
				{dataType : 'boolean', displayValue : 'Boolean'},
				{dataType : 'date', displayValue : 'Date'}
			];
			
	$scope.transformMethodOptions = [
			{transformMethod : 'date_diff_days', displayValue : 'Date difference in days'}, 
			{transformMethod : 'begins_with', displayValue : 'Begins with'}, 
			{transformMethod : 'not_empty', displayValue : 'Not empty'}
		];
	
	/**
	* Creates a new variable
	**/
	$scope.addVariable = function() {
		$scope.variables[$scope.newVariableName] = { 
			name: $scope.newVariableName, 
			isTransform : false, 
			dataType: 'int', 
			transformDefinition : {
				transformMethod : "begins_with",
				variables : [],
				arguments : []
			}
		};
		variableName:$scope.newVariableName = null;
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
		$scope.variables[$scope.variable.name][transformDefinition][transformMethod] = null;
	}
	
	$scope.addSummarySection = function() {
		$scope.summarySections[$scope.newSummarySectionName] = {}
		$scope.newSummarySectionName = null;
	}
	
	$scope.addSummaryVariable = function() {
		var summarySectionName = $scope.summarySectionName;
	}
	
	$scope.save = function() {
		// set the basic properties
		$scope.reportName = $scope.formReportName;
		$scope.description = $scope.formDescriptionText;
		
		jsonData = {"name" : $scope.reportName, "description" : $scope.description}
		
		// download the json file
		jsonDownload = angular.toJson(jsonData, pretty=true);
		
		window.location.href = "data:text;base64," + jsonDownload;
		document.location = 'data:Application/octet-stream,' + encodeURIComponent(jsonDownload);
		
		$scope.formReportName = null;
	};
	
}