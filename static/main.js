"use strict";
(function(){
  var style1 = [
    'color: #74e3ec',
    'line-height: 1.8;',
    'font-weight: bold;',
    'display: block'].join(';');
  var style2 = [
    'color: #07292c',
    'line-height: 1.8;',
    'font-weight: bold;',
    'display: block'].join(';');

  console.log('%c Hiring? %cGet in touch %c--> %ccontactMe() ', style1, style2, style1, style2);
})();

(function (){

  function toggleAccept(){
    // change the value to the ID of the UserChallenge (passed from server)
    console.log("post called sucess fn")
    // $('.accept-btn').text('Remove');

  };

  $('.accept-btn').on('click', function(e) {
    e.preventDefault()
    $.post('/accept.json', {'challenge_id':$(this).attr('data-challenge_id')}, toggleAccept);
  });



  // var login_modal = $('#login-popup')
  // var login_btn = $('#login')
  // var close = $('.close')


var modal = document.getElementById('login-popup');

   // Get the button that opens the modal
    var btn = document.getElementById("login");

   // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
      btn.onclick = function() {
          modal.style.display = "block";
      }

     // When the user clicks on <span> (x), close the modal
      span.onclick = function() {
          modal.style.display = "none";
      }

     // When the user clicks anywhere outside of the modal, close it
      window.onclick = function(event) {
          if (event.target == modal) {
              modal.style.display = "none";
          }
      }



})();

