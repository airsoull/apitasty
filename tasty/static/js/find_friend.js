$(document).on('ready', even);
function even(e){
  $('#search').on('click', function(e){
    e.preventDefault();

    $email_friend = $('#email_friend').val();
    $email = $('#email').val();

    $url = 'http://tasty.herokuapp.com/api/facebook/friend/?format=json';
    $url = $url + '&email=' + $email + '&email_friend=' + $email_friend;

    $.get($url, function(data, textStatus, xhr){
    }).success(function(data){
      console.log(data);
    }).fail(function(data, textStatus, xhr){
      console.log(xhr.status);
    });

  });
}