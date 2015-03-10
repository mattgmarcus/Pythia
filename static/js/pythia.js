$("#accept_loan_form").submit(function() {
  var self = this;

  $.ajax({
    type: "GET",
    url: "/predict",
    data: self.serialize()
  }).done(function(data) {
    $("#approval_result_container").show();
    $("#approval_result").html(data);
  });


  return false;
});
