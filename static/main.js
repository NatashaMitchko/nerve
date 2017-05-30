"use strict";
// Accept button IIFE

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

})();

// Log Out functions
(function(){
  function showLogout() {
    $('#logout').toggleClass('hidden');
      $('#caret').toggleClass('rotate');
  }
  $('#profile').on('click', showLogout);
})();


// Login/Register functions
(function(){
  // Toggle between login and register forms
  function toggleForm (){
    $('.main').toggleClass('hidden');
    $('.toggle-form').toggleClass('hidden');    
  }

  $('.toggle-form').on('click', toggleForm);

  // Form validation:
  // Check if username is taken
  // Make a request to server to check if username is taken
  function registerUsernameCheck(){
    var username = $('#register-username').val();
    $.get('/username_taken.json', {'username': username}, function(result){
      console.log(result);
      if (result['username-taken']){
        $('#register-message').text('Username is already taken');
      }
      else{
        $('#register-message').text('');
      }
    });
  }
  function loginUsernameCheck (){
    var username = $('#login-username').val();
    $.get('/username_taken.json', {'username': username}, function(result){
      if (!(result['username-taken'])){
        $('#login-message').text('User not found');
      }
      else{
        $('#login-message').text('');
      }
    });
  }
  $('#register-username').on('change', registerUsernameCheck);
  $('#login-username').on('change', loginUsernameCheck);

})();

// Timestamp button IIFE
(function (){

  function humanizeTime(){
    var that = this;
    $.get('/time.json', {'ISO_string':$(this).attr('data-timestamp')},
      function(result){
        $(that).text(result);
      }
    );
  };

  $('.time').each(humanizeTime);
})();


// Get matched tags (profile view)
(function(){
  function showAttributes(){
    var that = this;
    $.get('/matched_attributes.json', {'user_challenge_id':$(this).attr('data-challenge_id')},
      function(result){
        console.log(result);
        $.each(result, function(key) {
          console.log(key);
          $(that).append('<li>' + key + '</li>');
      });

      }
    );
  };
  $('.matched_attributes').each(showAttributes);

})();


// Count users IIFE
(function(){

  function getNumPlayers(){
    var that = this;
    $.get('/num-players.json', {'challenge_id':$(this).attr('data-challenge_id')},
      function(result){
        $(that).text(result);
      }
    );
  };

  $('.num-players').each(getNumPlayers);
})();


// So the user can only upload one file!
// $('.fileinput').change(function(){
//     if(this.files.length>10)
//         alert('to many files')
// });
// // Prevent submission if limit is exceeded.
// $('form').submit(function(){
//     if(this.files.length>10)
//         return false;
// });


// Secret 
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

  function contactMe(){
    window.open('/contact-me', '_blank'); 
    console.log('%c Talk to you soon!', style1);
  };
