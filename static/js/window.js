
$(".chosen-select").chosen({no_results_text: "No se encuentran registros..."}); 

// Chosen touch support.
if ($('.chosen-container').length > 0) {
    $('.chosen-container').on('touchstart', function(e){
      e.stopPropagation(); e.preventDefault();
      // Trigger the mousedown event.
      $(this).trigger('mousedown');
    });
  }

$(document).ready(function($) {
    $(document).find('.screen_data').load("../templates/index.html");

    $(document).on('click', '.btn_menu', function(event) {
        event.preventDefault();

        var screen_name = $(this).attr('screen_name');

        window.location.hash = '/' + screen_name;

        $(document).find('.screen_name').html(screen_name);;

        if (screen_name == "home") {
            $(document).find('.screen_data').load("../templates/index.html");
        } else if (screen_name == "details") {
            $(document).find('.screen_data').load("../templates/detail.html");
        }

    });

});

let comment = document.getElementById('review')
    let star = document.getElementById('review2')
    let btnEnviar = document.getElementById('send')

    btnEnviar.disabled = true
    console.log(comment.value.length)

    verificar = ()=> {
        if (comment.value.length > 10 && star.value.length === 1){
            
            btnEnviar.disabled = false;
        }else{
            btnEnviar.disabled = true
        }
    };