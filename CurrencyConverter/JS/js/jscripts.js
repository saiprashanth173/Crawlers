$(document).ready(function(){
	$('#resultsPage').hide();
	//$('#homePage').fadeIn(2000);
})


$.fn.setCursorPosition = function(pos) {
  this.each(function(index, elem) {
    if (elem.setSelectionRange) {
      elem.setSelectionRange(pos, pos);
    } else if (elem.createTextRange) {
      var range = elem.createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  });
  return this;
};

function getResultPage()
{
	//$('#resultsPage').hide();
	$('#homePage').hide();
	$('#resultsPage').show();
	var formValue=$('#homeForm').val();
	$('#queryBox').val(formValue).focus();
	$('#queryBox').setCursorPosition(formValue.length);
	$('#clusters').hide();
}

function getClusters(){
	$('#clusters').toggle();
  $('#queryBox').focus();
}


function showResults()
{
  var placeString="<div class='container-fluid'>";
  for (i=0;i<10;i++)
  {
    placeString=placeString+"<div class='row-fluid'><div class='resultDiv'><div class='row-fluid'><div class'title'><a class='links' href='#'><h4>This is a test link which is used for testing only for testing</h4></a></div></div><div class='row-fluid'><div class'ref'>http://www.testlink.com</div></div></div></div>";
  }

  $('#results').html(placeString+"</div>");
}