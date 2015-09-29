$(document).ready(function(){

	$.get('http://localhost/cgi-bin/getCurrency.py',{},function(data){
		var response = JSON.parse(data);
		showDetails(response);
	});
});