$(document).ready(function(){
	//$("#left1").hide();
	$("#ctr").hide();
	$("#ctr1").hide();
	//$(".cleft-i").hide();
	$(".ctrending").hide();
	$(".ccluster").hide();
	$("#trend").click(function(){
		$("#header").delay(800).animate({
			marginTop:'0',
			marginLeft:'0'
		})
		$('#ctrend').delay(100).animate({fontSize: '50px'},300);
		$("#ctrend").delay(200).animate({
			marginLeft:' ',
			marginTop:'10'		
		})
		$("#cleft1").delay(1200).animate({
			marginTop:' -400',
			marginLeft:'1000'
		})
		$("#cleft2").delay(1400).animate({
			marginTop:' -340',
			marginLeft:'1000'
		})
		$("#cleft3").delay(1600).animate({
			marginTop:' -280',
			marginLeft:'1000'
		})
		$("#ccont").css('background-color','#fff');
		//$("#c1").slideDown();	
		$(".ctrending").show("slow");
	})
	$("#cleft1").click(function(){
		go();
		$("#cleft1").css('background-color','#c0392b');
		$("#cleft1").css('color','#fff');
		nav();
		$("#cc1").show("slow");
		
	})
	$("#cleft2").click(function(){
		go()
		$("#cleft2").css('background-color','#2980b9');
		$("#cleft2").css('color','#fff');
		nav();
		$("#cc2").show("slow");
		
	})
	$("#cleft3").click(function(){
		go();
		$("#cleft3").css('background-color','#d35400');
		$("#cleft3").css('color','#fff');
		nav();
		$("#cc3").show("slow");
		
	})
	function go(){
		$(".cleft-i").css('color','#fff');
		$(".cleft-i").css('background-color','#3498db');
		$(".left-i").css('color','#fff');
		$(".left-i").css('background-color','2ecc71');
		$(".ccluster").fadeOut();
		$(".left-i").hide();
		$("#ctrend").slideUp('slow');
	}
	function nav(){
		$("#cleft1").delay(200).animate({
			marginLeft:'250',
			marginTop:'-480'
		})
		$("#cleft2").delay(400).animate({
			marginLeft:'550',
			marginTop:'-480'
		})
		$("#cleft3").delay(600).animate({
			marginLeft:'850',
			marginTop:'-480'
		})
	}
		
})