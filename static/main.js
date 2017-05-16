"use strict";

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

