$(document).ready(function()
{
	$('.diftabs').hide(); 
	$('#home').show();
	$.get('http://localhost/cgi-bin/miniproject/temp.py',{},function(data){
		var gets = $.parseJSON(data);
		$("#temp").html("<b>"+gets["Temp"]+"&deg;"+"C</b>");
		$("#humid").html("<b>"+gets["Humidity"]+" %</b>");
	});


});

var i=0;
function makeCall(vals)
{
	if (i==0)
	{
	send = {"keyword":JSON.stringify(vals)};
	$.get('http://10.42.0.88/cgi-bin/on.py',send, function(data){});
	i=1;
	}
	else if(i==1 ){
	send = {"keyword":JSON.stringify(vals)};
	$.get('http://10.42.0.88/cgi-bin/off.py',send, function(data){});	
	i=0;
	}			

}


function performCall()
{
	if (i==0)
	{
	$("#fanDiv").addClass("fan");
	send = {"keyword":"on"};
	$.get('http://10.42.0.88/cgi-bin/fanon.py',send, function(data){});
	i=1;	
	}
	else if(i==1)
	{

	$("#fanDiv").removeClass("fan");
	//$(".fan").css("animation-name", "none");
	send = {"keyword":"off"};
	$.get('http://10.42.0.88/cgi-bin/fanon.py',send, function(data){});
	i=0;
	}
}