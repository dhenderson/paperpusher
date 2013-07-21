var report_data = {"name" : "New report"}

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