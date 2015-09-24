/**
 * felix.shaw@tgac.ac.uk - 22/09/15.
 */

$(document).ready(function () {
    $('#test_wizard').on('click', process_stage)
    $('#file-carousel').on('slide.bs.carousel', function () {
        alert('cock')
    })
    $('#file_info_send').on('click', process_stage)
    $('#file-carousel').carousel({
        interval: 0
    })
})

function process_stage() {
    var study_type = $('#study_type').val()
    $.ajax({
        type: 'get',
        url: '/rest/get_next_wizard_stage/',
        dataType: 'json',
        data: {'study_type': study_type, 'prev_question': ''}
    }).done(function (d) {
        var html = d.detail
        var x = $(html).wrap('<div class="item active"></div>')
        $('#file_slides').append(html)


        $('#file_slides').append(
            '<div class="item"><div class="text-center"><div class="lead">Select Parameter Value[library strategy]</div><select class="form-control" name="studies.study.assays.assaysTable.genomeSeq.libraryConstruction.libraryStrategy" id="studies.study.assays.assaysTable.genomeSeq.libraryConstruction.libraryStrategy"><option>AMPLICON</option><option>CLONE</option><option>WGS</option><option>OTHER</option></select></div></div>'
        )


        $('#filesAssignModal').modal('show')
    })
}