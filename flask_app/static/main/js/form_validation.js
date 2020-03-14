window.onload = function() { 

$('.hide_till_end').hide();
$('.hide_init').hide();

$('#hide_btn_1').click(function(){
    $('.group-1').hide();
    $('.group-2').show();
})

$('#hide_btn_2').click(function(){
    $('.group-2').hide();
    $('.group-3').show();
})

$('#hide_btn_3').click(function(){
    $('.group-3').hide();
    $('.group-4').show();
})

$('#hide_btn_4').click(function(){
    $('.group-4').hide();
    $('.group-5').show();
})

$('#hide_btn_5').click(function(){
    $('.group-5').hide();
    $('.group-6').show();
})

$('#hide_btn_6').click(function(){
    $('.group-6').hide();
    $('.group-7').show();
})

$('#hide_btn_7').click(function(){
    $('.group-7').hide();
    $('.group-8').show();
})

$('#hide_btn_8').click(function(){
    $('.group-8').hide();
    $('.group-9').show();
})

$('#hide_btn_9').click(function(){
    $('.hide_init').hide();
    $('.group-9').hide();
    $('.form-group').show();
    $('.hide_till_end').show();
    $('.form-control').show();
    $('.question_body_container').css("align-items", "initial");
})

};
