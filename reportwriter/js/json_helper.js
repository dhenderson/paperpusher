function check_browser(){
	// Check for the various File API support.
	if (window.File && window.FileReader && window.FileList && window.Blob) {
	  // Great success! All the File APIs are supported.
	} else {
	  alert('The File APIs are not fully supported in this browser.');
	}
}

function handleFileSelect(evt) {
	var files = evt.target.files; // FileList object

	// files is a FileList of File objects. List some properties.
	var output = [];
	for (var i = 0, f; f = files[i]; i++) {
	  output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
				  f.size, ' bytes, last modified: ',
				  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
				  '</li>');
	}
	document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}
document.getElementById('files').addEventListener('change', handleFileSelect, false);

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