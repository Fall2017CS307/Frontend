$(document).ready(function() {
	// Header Scroll
	$(window).on('scroll', function() {
		var scroll = $(window).scrollTop();

		if (scroll >= 50) {
			$('#header').addClass('fixed');
		} else {
			$('#header').removeClass('fixed');
		}
	});

	// Fancybox
	$('.work-box').fancybox();

	// Flexslider
	$('.flexslider').flexslider({
		animation: "fade",
		directionNav: false,
	});

	// Page Scroll
	var sections = $('section')
		nav = $('nav[role="navigation"]');

	$(window).on('scroll', function () {
	  	var cur_pos = $(this).scrollTop();
	  	sections.each(function() {
	    	var top = $(this).offset().top - 76
	        	bottom = top + $(this).outerHeight();
	    	if (cur_pos >= top && cur_pos <= bottom) {
	      		nav.find('a').removeClass('active');
	      		nav.find('a[href="#'+$(this).attr('id')+'"]').addClass('active');
	    	}
	  	});
	});
	nav.find('a').on('click', function () {
	  	var $el = $(this)
	    	id = $el.attr('href');
		$('html, body').animate({
			scrollTop: $(id).offset().top - 75
		}, 500);
	  return false;
	});

	// Mobile Navigation
	$('.nav-toggle').on('click', function() {
		$(this).toggleClass('close-nav');
		nav.toggleClass('open');
		return false;
	});	
	nav.find('a').on('click', function() {
		$('.nav-toggle').toggleClass('close-nav');
		nav.toggleClass('open');
	});
	
	//Modal
	$("#myModal .forgot-password").click(function(evt) {
 		$("#myModal .login-div").fadeOut(100);
    	$("#myModal .reset-div").fadeIn(100);
	});

	$("#myModal .back").click(function(evt) {
 		$("#myModal .reset-div").fadeOut(100);
 		$("#myModal .registration-div").fadeOut(100);
    	$("#myModal .login-div").fadeIn(100);
	});

	$("#log-in-btn").click(function(evt) {
 		$("#myModal .reset-div").fadeOut(100);
 		$("#myModal .registration-div").fadeOut(100);
    	$("#myModal .login-div").fadeIn(100);
	});

	$("#myModal .sign-up").click(function(evt) {
 		$("#myModal .login-div").fadeOut(100);
    	$("#myModal .registration-div").fadeIn(100);
	});

	
});