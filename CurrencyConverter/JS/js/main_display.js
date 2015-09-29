var countries=['Mauritian Rupee', 'Bruneian Dollar', 'Botswana Pula', 'Bulgarian Lev', 'Chinese Yuan Renminbi', 'Thai Baht', 'Japanese Yen', 'Swedish Krona', 'Croatian Kuna', 'Brazilian Real', 'Nepalese Rupee', 'US Dollar', 'Qatari Riyal', 'Mexican Peso', 'Indonesian Rupiah', 'Taiwan New Dollar', 'Canadian Dollar', 'Polish Zloty', 'Icelandic Krona', 'Trinidadian Dollar', 'Iranian Rial', 'Omani Rial', 'Malaysian Ringgit', 'Euro', 'Philippine Peso', 'Saudi Arabian Riyal', 'Libyan Dinar', 'Hungarian Forint', 'Australian Dollar', 'Venezuelan Bolivar', 'Indian Rupee', 'Argentine Peso', 'Swiss Franc', 'Kuwaiti Dinar', 'New Zealand Dollar', 'Chilean Peso', 'Pakistani Rupee', 'Singapore Dollar', 'Czech Koruna', 'Norwegian Krone', 'Danish Krone', 'Hong Kong Dollar', 'Bahraini Dinar', 'Russian Ruble', 'Romanian New Leu', 'Turkish Lira', 'Kazakhstani Tenge', 'South Korean Won', 'Emirati Dirham', 'Colombian Peso', 'Sri Lankan Rupee', 'Israeli Shekel', 'South African Rand', 'British Pound'];

$(document).ready(function(){

	/*var to="";
	for(i=0;i<countries.length;i++)
	{
		to+="<option value='"+countries[i]+"' onclick='javascript:call_fun(\""+countries[i]+"\")'>"+countries[i]+"</option>";
	}
	$("#to_select").html(to);*/
});


function showDetails(response)
{
alert(response);
}


function call_fun(name)
{
	alert(name);
}