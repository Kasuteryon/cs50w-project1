
$(document).ready(function($) 
	{
		$(document).find('.screen_data').load("../index.html");

 		$(document).on('click', '.btn_menu', function(event) 
 		{
 			event.preventDefault();

 			var screen_name = $(this).attr('screen_name'); 			

 			window.location.hash = '/'+screen_name;

 			$(document).find('.screen_name').html(screen_name);;

 			if(screen_name == "home")
 			{ 
 				$(document).find('.screen_data').load("../index.html");
 			}
 			else if(screen_name =="saved")
 			{ 
 				$(document).find('.screen_data').load("../saved.html"); 				
			}
			else if(screen_name =="details")
 			{ 
 				$(document).find('.screen_data').load("../detail.html"); 				
			}  			 

 		});
 
	});

	