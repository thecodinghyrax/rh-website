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
    $('.form-group').show();
    $('.hide_till_end').show();
    $('.question_body_container').css("align-items", "initial");
})

// myArray = [];
// function valTextField() {
//     console.log("The valTextField function was called");
    
//     var x = document.form["applyForm"]["ApplyName"].value;
//     if (x == "") {
//         alert("This is a required field. Please enter your name.");
//     } else {
//         alert("Way to go")
//     }
// };

// var nameBtn = document.getElementById('nameContinue')
// nameBtn.addEventListener("click", valTextField);
// $('#cont1').click(function(){
    
//     myArray.push($('#name').val());
//     console.log(myArray);
    
// });
// $('#cont2').click(function(){
    
//     myArray.push($('input:radio[name=join_how]:checked').val());
//     console.log(myArray);
    
// });

// $('#find_how-4').click(function(){
//     $('#otherLabel').hide();
//     $('#find_how-4').replaceWith("<input id='otherTextBox' type='text'name='find_how'>");

// });
// $('#cont3').click(function(){
//     if ($('input:radio[name=find_how]:checked').val() == undefined) {
//         myArray.push($('#otherTextBox').val());
//     } else {
//         myArray.push($('input:radio[name=find_how]:checked').val());
//     }
//     console.log(myArray);
    
// });
// $('#cont4').click(function(){
    
//     myArray.push($('#self_description').val());
//     console.log(myArray);
    
// });
// $('#cont5').click(function(){
    
//     myArray.push($('#b_tag').val());
//     console.log(myArray);
    
// });
// $('#cont6').click(function(){
    
//     myArray.push($('#play_when').val());

//     $('.formResults').append("<form name='applyForm' method='POST' action='/apply'>");
//     console.log(myArray);
    
//     $('.formResults').append("<input type='text' name='name' value='" + myArray[0] + "'>Name</input>");
//     $('.formResults').append("<input type='text' name='join_how' value='" + myArray[1] + "'>How will you be joining us?</input>");
//     $('.formResults').append("<input type='text' name='find_how' value='" + myArray[2] + "'>How did you find us?</input>");
//     $('.formResults').append("<input type='text' name='description' value='" + myArray[3] + "'>Your personal description: </input>");
//     $('.formResults').append("<input type='text' name='b_tag' value='" + myArray[4] + "'>Battle Tag?</input>");
//     $('.formResults').append("<input type='text' name='play_when' value='" + myArray[5] + "'>What times do you normal play?</input>");
//     $('.formResults').append("<button id='formSubmitBtn'>Submit Application</button>");
//     $('.formResults').append("</form>");

// });



};
