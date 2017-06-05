"use strict";
// Accept button IIFE (Works both on challenge list and challenge details page)

(function (){

  function toggleAccepted(button){
    // accept-btn > span
    // console.log(button);
    $(button).prop('disabled', true);
    $(button).children().removeClass('glyphicon-plus');
    $(button).children().addClass('glyphicon-ok');
    $(button).children().addClass('ok-accepted');

    // console.log("called toggleAccepted");
  }

  function toggleCompleted(button){
    // console.log(button);
    $(button).prop('disabled', true);
    $(button).children().removeClass('glyphicon-plus');
    $(button).children().addClass('glyphicon-ok');
    $(button).children().addClass('ok-finished');
    // console.log("called toggleCompleted");

  }

  function isCompleted(){
    var that = this;
    $.get('/is_completed.json', {'challenge_id':$(this).attr('data-challenge_id')},
      function (results){
        // console.log(results);
        // console.log($(this).attr('data-challenge_id'));
        if (results['status'] == 'accepted'){
          toggleAccepted(that); 
        }
        else if (results['status'] == 'completed'){
          toggleCompleted(that);
        }

      } );
  }

  $('.accept-btn').each(isCompleted);
  $('.accept-btn').on('click', function(e) {
    e.preventDefault();

    var btn = $(this);
    $.post('/accept.json', {'challenge_id':btn.attr('data-challenge_id')}, 
      function (results){ toggleAccepted(btn); } );
  });

})();

// Add new challenge button
(function(){
  function toggleForm (){
    var form = $('#create-new-form');
    if (form.hasClass('hidden')){
      console.log('has class hidden');
      form.removeClass('hidden');
    }
    else {
            console.log('does not have class hidden');
      form.addClass('hidden');
    }
    // $('#create-new-form').toggleClass('hidden');
    $('#create-new-btn').toggleClass('rotate45');
  }

  $('#create-new-btn').on('click', toggleForm);
})();

// Log Out functions
(function(){
  function showLogout() {
    $('#logout').toggleClass('hidden');
      $('#caret').toggleClass('rotate180');
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
  $('.matched-attributes').each(showAttributes);

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

// Participants/ completed for doughnut graph
(function(){
  function makeChart(result){

  var myChart = new Chart(document.getElementById("chartjs-completed"),
    {"type":"doughnut",
    "data":{
      "labels":["Finished", "In Progress"],
      "datasets":[{
        "label":"Progress",
        "data":[result['finished'], result['unfinished']],
        "backgroundColor":["rgb(232, 232, 238)","rgb(103,219,228)"]}]
          }
      });
  }

  $.get('/completion-stats.json', {'challenge_id':challenge_id}, makeChart);

})();

// Insert form at the top of the challenges page when + is clicked
(function(){

  function toggleCreateForm(){
    //////////////////////////////////////////////////////////////////////////////////// make form styled and hidden then toggle back and forth w/ + button
  }

  $('#create-new-btn').on('click', toggleCreateForm);

})();


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
