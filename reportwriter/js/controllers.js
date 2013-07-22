function ReportController($scope) {
	
	$scope.reportName = null;
	$scope.description = null;
	$scope.variables = {};
	
	$scope.addVariable = function() {
		$scope.variables[$scope.newVariableName] = { name: $scope.newVariableName, isTransform : false};
		variableName:$scope.newVariableName = null;
	}
	
	$scope.removeVariable = function(variableName) {
		delete $scope.variables[variableName];
	}
	
	$scope.save = function() {
		// set the basic properties
		$scope.reportName = $scope.formReportName;
		$scope.description = $scope.formDescriptionText;
		
		jsonData = {"name" : $scope.reportName, "description" : $scope.description}
		
		$scope.formReportName = null;
	};
	
}