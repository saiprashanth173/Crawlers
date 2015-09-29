$(document).ready(function(){
	//$("#left1").hide();
	$("#tr").hide();
	$("#tr").hide();
	$("#c4").hide();
	$(".trending").click(function(){
		$(".ccluster").hide();
		$(".cluster").hide();
		nav2();
		$(".left-i").css('background-color','#2ecc71');
		$(".left-i").css('color','#fff ');
		$(".cleft-i").css('background-color','#3498db ');
		$(".cleft-i").css('color','#fff');		
		$(".left-i").show("slow");
		$("#c4").slideDown("slow");
	})
	$(".ctrending").click(function(){
		$(".cluster").hide();
		$(".ccluster").hide();
		nav1();
		$(".left-i").css('background-color','#2ecc71');
		$(".left-i").css('color','#fff ');
		$(".cleft-i").css('background-color','#3498db ');
		$(".cleft-i").css('color','#fff');
		$(".cleft-i").show("slow");
		$("#c5").slideDown('slow');
	})
	$(".trending").hide();
	$(".cluster").hide();
	$("#trend").click(function(){

		$("#header").delay(800).animate({
			marginTop:'0',
			marginLeft:'0'
		})
		$('#trend').delay(100).animate({fontSize: '50px'},300);
		$("#trend").delay(200).animate({
			marginLeft:' ',
			marginTop:'10'		
		})
		$("#left1").delay(1200).animate({
			marginTop:' 100',
			marginLeft:'0'
		})
		$("#left2").delay(1400).animate({
			marginTop:' 160',
			marginLeft:'0'
		})
		$("#left3").delay(1600).animate({
			marginTop:' 220',
			marginLeft:'0'
		})
		$("#cont").css('background-color','#fff');
		//$("#c1").slideDown();	
		$(".trending").show("slow");
	})
	$("#left1").click(function(){
		go();
		$("#left1").css('background-color','#c0392b');
		$("#left1").css('color','#fff');
		nav();
		$("#c1").show("slow");
		
	})
	$("#left2").click(function(){
		go()
		$("#left2").css('background-color','#2980b9');
		$("#left2").css('color','#fff');
		nav();
		$("#c2").show("slow");
		
	})
	$("#left3").click(function(){
		go();
		$("#left3").css('background-color','#d35400');
		$("#left3").css('color','#fff');
		nav();
		$("#c3").show("slow");
		
	})
	function go(){
		$(".left-i").css('color','#fff');
		$(".left-i").css('background-color','#2ecc71');
		$(".cleft-i").css('color','#fff');
		$(".cleft-i").css('background-color','#3498db');
//		$("body").css('background',' ');
		$(".cluster").fadeOut();
		//$("#trend").slideUp('slow');
		$(".cleft-i").hide();
	}
	function nav(){
		$("#left1").delay(200).animate({
			marginLeft:'250',
			marginTop:'80'
		})
		$("#left2").delay(400).animate({
			marginLeft:'550',
			marginTop:'80'
		})
		$("#left3").delay(600).animate({
			marginLeft:'850',
			marginTop:'80'
		})
	}
	function nav1(){
		$("#left1").delay(200).animate({
			marginTop:' 100',
			marginLeft:'0'
		})
		$("#left2").delay(400).animate({
			marginTop:' 160',
			marginLeft:'0'
		})
		$("#left3").delay(600).animate({
			marginTop:' 220',
			marginLeft:'0'
		})
		
	}
	function nav2(){
		$("#cleft1").delay(200).animate({
			marginTop:' -400',
			marginLeft:'1000'
		})
		$("#cleft2").delay(400).animate({
			marginTop:' -340',
			marginLeft:'1000'
		})
		$("#cleft3").delay(600).animate({
			marginTop:' -280',
			marginLeft:'1000'
		})
		
	}
		
})