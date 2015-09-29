$(document).ready(function(){$('.diftabs').hide(); $('#home').show();});
function signup()
{
	window.open("./signup.html","_self");
}

function login()
{
	window.open("./main.html","_self");
}

function changediv(val){
	$('.diftabs').hide(); 
	$('#'+val).show();
}