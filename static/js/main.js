(function($) {
    'use strict';
	
	jQuery(document).ready(function(){
		
		/* START MENU-JS */	
			$('.nav a').on('click', function(e){
				var anchor = $(this);
				$('html, body').stop().animate({
					scrollTop: $(anchor.attr('href')).offset().top - 50
				}, 1500);
				e.preventDefault();
			});		

	
			$(window).scroll(function() {
			  if ($(this).scrollTop() > 100) {
				$('.menu-top').addClass('menu-shrink');
			  } else {
				$('.menu-top').removeClass('menu-shrink');
			  }
			});
			
			$(document).on('click','.navbar-collapse.in',function(e) {
			if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
				$(this).collapse('hide');
			}
			});				
		/* END MENU-JS */
		
		/* START MOBILE-MENU  */
			$('.main_menu').slicknav({
				prependTo:".mobile-nav",
			});
		/* START MOBILE-MENU  */
		 
		/* START ISOTOP JS */
			var $grid = $('.work_content_area').isotope({
			  // options
			});
			// filter items on button click
			$('.work_filter').on( 'click', 'li', function() {
			  var filterValue = $(this).attr('data-filter');
			  $grid.isotope({ filter: filterValue });
			});
			// filter items on button click
			$('.work_filter').on( 'click', 'li', function() {
				$(this).addClass('active').siblings().removeClass('active')
			});
		/* END ISOTOP JS */
		
		/* START LIGHTBOX */
		
			lightbox.option({
			  'resizeDuration': 200,
			  'wrapAround': true
			});
		
		/* END LIGHTBOX JS */
		
		/* START COUNDOWN JS */

$('#counter_area').on('inview', function(event, visible, visiblePartX, visiblePartY) {
    if (visible) {
        $(this).find('.counter').each(function () {
            var $this = $(this);
            var finalValue = parseFloat($this.text().replace(',', '')); // Зчитування числа з десятковими знаками
            $({ Counter: 0 }).animate({ Counter: finalValue }, {
                duration: 5000,
                easing: 'swing',
                step: function (now) {
                    $this.text(Math.floor(now)); // Відображення без десяткових знаків і без коми
                }
            });
        });
        $(this).unbind('inview');
    }
});

		/* END COUNDOWN JS */
		
		/* START TESTIMONIAL JS */
			$(".testmonial_slider_area").owlCarousel({
				autoPlay: true,
				slideSpeed:1000,
				items : 3,
				loop: true,
//				nav:true,
//				navText:['<i class="ti-arrow-left"></i>','<i class="ti-arrow-right"></i>'],
				margin: 30,
				dots: true,
				responsive:{
					320:{
						items:1
					},
					767:{
						items:2
					},
					600:{
						items:2
					},
					1000:{
						items:3
					}
				}
				
			});
		/* END TESTIMONIAL JS */
	});	
	
		/*PRELOADER JS*/
//			$(window).on('load', function() {
//				$('.spinner').fadeOut();
//				$('.preloader').delay(350).fadeOut('slow');
//			});
		/*END PRELOADER JS*/
		
		// Wow
			new WOW().init();
})(jQuery);