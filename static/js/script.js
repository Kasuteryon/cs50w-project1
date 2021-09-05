
document.addEventListener("DOMContentLoaded", (event) => {

	const showNavbar = (toggleId, navId, bodyId, headerId) =>{
		const toggle = document.getElementById(toggleId),
		nav = document.getElementById(navId),
		bodypd = document.getElementById(bodyId),
		headerpd = document.getElementById(headerId)
		
		// Validate that all variables exist
		if(toggle && nav && bodypd && headerpd){
			toggle.addEventListener('click', ()=>{
			// show navbar
			nav.classList.toggle('show')
			// change icon
			toggle.classList.toggle('bx-x')
			// add padding to body
			bodypd.classList.toggle('body-pd')
			// add padding to header
			headerpd.classList.toggle('body-pd')
		})
	}
}
		
showNavbar('header-toggle','nav-bar','body-pd','header')

	
const linkColor = document.querySelectorAll('.nav_link')
		
const colorLink = () => {
	if(linkColor){
		linkColor.forEach(l=> l.classList.remove('active'))
		this.classList.add('active')
	}
}

linkColor.forEach(l => l.addEventListener('click', colorLink))
		
	
});

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

 		});
 
	});