/**
 * felix.shaw@tgac.ac.uk - 22/09/15.
 */

$(document).ready(function() {
  $('#test_wiz').on('click', process_stage);

  if ($('#wizard').is(':empty')) {
    $('#test_wizard').on('click', process_stage)
  } else {
    $('#filesAssignModal').modal('show')
  }
});

function process_stage() {
  var study_type = $('#study_type').val();
  var prev_step_id;
  try {
    var current_step = $('#wizard').steps('getCurrentStep');
    prev_question = $(current_step).data('step_id')
  }
  catch(Error){
    prev_question = ''
  }
  //console.log(current_step.title)
  $.ajax({
    type: 'get',
    url: '/rest/get_next_wizard_stage/',
    dataType: 'json',
    data: {
      'study_type': study_type,
      'prev_question': prev_question
    }
  }).done(function(d) {
    $('#wizard').steps('add', {
      title: d.detail.title,
      content: d.detail.element
    });
    var num_steps = $('#wizard').find('section').length;
    while (num_steps > 1 && $('#wizard').steps('next')) {}
    //assign id to current wizard step
    current_step = $('#wizard').steps('getCurrentStep');
    $(current_step).data('step_id', d.detail.id);
    $('#filesAssignModal').modal('show')
  })
}
