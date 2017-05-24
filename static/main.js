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
    $.get('/matched_attributes.json', {'challenge_id':$(this).attr('data-challenge_id')},
      function(result){
        for (var i = 0; i<result.length; i++){
          var attribute = $("<li>"+result[i]+"/li");
          $(that).append(attribute);
        };
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
