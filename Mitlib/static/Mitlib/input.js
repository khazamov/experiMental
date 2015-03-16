function get(el) {
  return document['querySelector' + (el.indexOf('#') === 0 ? '' : 'All')](el);
}

function getTimeStamp(dateString) {
  return new Date(dateString).getTime() / 1000;
}
//
//function reset() {
//  var inputs = get('input[type=text]');
//  [].forEach.call(inputs, function(input) {
//    input.value = '';
//  });
//  get('#link').style.display = 'none';
//  get('#getLink').style.display = 'inline-block';
//  get('#subReddit').focus();
//}

//get('#getLink').addEventListener('click', function() {
//  var subReddit = get('#subReddit').value.replace(/\s/g, ''),
//      startTime = getTimeStamp(get('#startDate').value),
//      endTime   = getTimeStamp(get('#endDate').value);
//
//  var all = (subReddit.toLowerCase() === 'all' || subReddit === '');
//
//  var url = "http://reddit.com/search?q=" + (all ? '' : ("(and+subreddit%3A'" + subReddit + "'")) + "timestamp%3A" + startTime + ".." + endTime + (all ? '' : ')') + "&amp;syntax=cloudsearch";
//
//  this.style.display = 'none';
//
//  var linkButton = get('#link');
//
//  linkButton.href = url;
//  linkButton.style.display = 'inline-block';
//
//
//});

//get('#link').addEventListener('click', function() {
//  reset();
//});

$('#date_start').datepicker();

$("#endDate").datepicker();

$('.input-group-addon').on('click', function() {
  $(this).next('input').focus();
});




angular.module('myModule', ['ui.bootstrap']);

angular.module('ui.bootstrap.demo').controller('AlertDemoCtrl', function ($scope) {
  $scope.alerts = [
    { type: 'danger', msg: 'Oh snap! Change a few things up and try submitting again.' },
    { type: 'success', msg: 'Well done! You successfully read this important alert message.' }
  ];

  $scope.addAlert = function() {
    $scope.alerts.push({msg: 'Another alert!'});
  };

  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };
});


