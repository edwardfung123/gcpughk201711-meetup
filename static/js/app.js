$(document).ready(function() {
  var $app = $('#app');
  var $debug = $app.find('#debug');
  $app.find('#send-btn').click(function(e) {
    e.preventDefault();
    var now = new Date();
    var html = now.toISOString() + '\n' ;
    $debug.prepend(html)
  });
  console.log('xxx');
  // console.log('asd');
});
