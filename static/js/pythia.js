$(function() {
  $('#submit_button').bind('click', function() {
    $.getJSON('/predict', {
      loan_amount: $('input[name="loan_amount"').val(),
      debt_to_income: $('input[name="debt_to_income"').val(),
      zip_code: $('input[name="zip_code"').val(),
      address_state: $('input[name="address_state"').val(),
      employment_length: $('input[name="employment_length"').val()
    }, function(data) {
      $('#approval_result_container').show();
      $('#approval_result').text(data.result);
    });

    return false;
  });
});
