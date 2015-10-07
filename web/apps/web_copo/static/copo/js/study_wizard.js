/**
 * felix.shaw@tgac.ac.uk - 22/09/15.
 */

$(document).ready(function () {
    $('#next_wiz').on('click', next_step);
    $('#prev_wiz').on('click', prev_step);


    $('#test_wizard').on('click', handle_click)

});

function handle_click() {
    if ($('#wizard').find('section').length == 0) {
        process_stage(false)
    }
    else {
        $('#filesAssignModal').modal('show')
    }
}

function next_step() {
    var num_steps = $('#wizard').find('section').length;
    var wizard_steps;
    try {
        wizard_steps = $('#wizard').data('num_steps')
    }
    catch (Error) {
        wizard_steps = 0
    }
    if ($('#wizard').steps('getCurrentIndex') < num_steps - 1) {
        $('#wizard').steps('next')
    }
    else {
        if (num_steps == wizard_steps) {
            process_stage(true)
        }
        else {
            process_stage(false)
        }
    }
}

function process_stage(last_stage) {
    var study_type = $('#study_type').val();
    var prev_step_id;
    var prev_question;
    var current_answer = '';
    var current_step;
    try {
        current_step = $('#wizard').steps('getCurrentStep');
        prev_question = $(current_step).data('step_id')
    }
    catch (Error) {
        current_step = undefined;
        prev_question = ''
    }

    if (current_step != undefined) {
        current_answer = $('section:visible').find('.input-copo').val()
    }


    data_dict = {
        'answer': current_answer,
        'study_type': study_type,
        'prev_question': prev_question
    };

    if(last_stage)
        data_dict.last = true;
    else
        data_dict.last = false;

    $.ajax({
        type: 'get',
        url: '/rest/get_next_wizard_stage/',
        dataType: 'json',
        data: data_dict
    }).done(function (d) {
        if (last_stage) {
            $('#filesAssignModal').modal('hide')
        }
        else {
            $('#wizard').steps('add', {
                title: d.detail.title,
                content: d.detail.element
            });

            $('#wizard').data('num_steps', d.num_steps);
            var num_steps = $('#wizard').find('section').length;
            while (num_steps > 1 && $('#wizard').steps('next')) {
            }
            current_step = $('#wizard').steps('getCurrentStep');
            $(current_step).data('step_id', d.detail.id);
            $('.ontology-term').css('color', 'red');
            $('#filesAssignModal').modal('show')
        }
    })
}

function prev_step() {
    $('#wizard').steps('previous')
}
