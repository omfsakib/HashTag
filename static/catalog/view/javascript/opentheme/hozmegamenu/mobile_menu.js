$(document).ready(function () {
	$("#ma-mobilemenu .had_child, ul.mobilemenu li span.button-view1, ul.mobilemenu li span.button-view2").each(function(){
        $(this).append('<span class="ttclose"><a href="javascript:void(0)"></a></span>');
      });
	$("ul.mobilemenu li.active").each(function(){
		$(this).children().next("ul").css('display', 'block');
	});
	$("ul.mobilemenu li ul").hide();
	
	// only category menu
	$('span.button-view1 span').click(function() { 
	if ($(this).hasClass('ttopen')) {varche = true} else {varche = false};
	if(varche == false){
		$(this).addClass("ttopen");
		$(this).removeClass("ttclose");
		$(this).parent().parent().find('ul.level2').slideDown();
		varche = true;
	} else 
	{	
		$(this).removeClass("ttopen");
		$(this).addClass("ttclose");
		$(this).parent().parent().find('ul.level2').slideUp();
		varche = false;
	}
	});
	$('span.button-view2 span').click(function() { 
		if ($(this).hasClass('ttopen')) {varche = true} else {varche = false};
		if(varche == false){
			$(this).addClass("ttopen");
			$(this).removeClass("ttclose");
			$(this).parent().parent().find('ul.level3').slideDown();
			varche = true;
		} else 
		{	
			$(this).removeClass("ttopen");
			$(this).addClass("ttclose");
			$(this).parent().parent().find('ul.level3').slideUp();
			varche = false;
		}
	});
	
	// origin menu
	$('#ma-mobilemenu li.had_child').click(function(){
		var chk = 0;
		if ( $(this).children('span').hasClass('ttclose') && ( chk==0 ) ) {
			$(this).children('span').removeClass('ttclose');
			$(this).children('span').addClass('ttopen');
			$(this).children('ul').slideDown();
			chk = 1;
		}
		if ( $(this).children('span').hasClass('ttopen') && ( chk==0 ) ) {
			$(this).children('span').removeClass('ttopen');
			$(this).children('span').addClass('ttclose');
			$(this).children('ul').slideUp();
			chk = 1;
		}
	});
	//mobile
	$('.btn-navbar').click(function() {
		var chk = 0;
		if ( $('#navbar-inner').hasClass('navbar-inactive') && ( chk==0 ) ) {
			$('#navbar-inner').removeClass('navbar-inactive');
			$('#navbar-inner').addClass('navbar-active');
			$('#ma-mobilemenu').slideDown();
			chk = 1;
		}
		if ($('#navbar-inner').hasClass('navbar-active') && ( chk==0 ) ) {
			$('#navbar-inner').removeClass('navbar-active');
			$('#navbar-inner').addClass('navbar-inactive');			
			$('#ma-mobilemenu').slideUp();
			chk = 1;
		}
		//$('#ma-mobilemenu').slideToggle();
	});    
});