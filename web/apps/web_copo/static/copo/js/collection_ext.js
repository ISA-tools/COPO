$(document).ready(function () {

    //handle event for date picker
    $('.pop_date_picker').datepick({
        dateFormat: 'D, M d, yyyy',
        altField: '#isoDate', altFormat: 'yyyy-mm-dd'
    });

    //handle event for add new study type
    $('#btn_add_new_study_type').on('click', function () {
        do_add_new_study_type();
    });

    function do_add_new_study_type() {
        var $candidates = $('input[name=add_new_study_type]:checked');

        if ($candidates.length > 0) {
            var study_types = [];
            $candidates.each(function () {
                study_types[study_types.length] = $(this).val();
            });

            study_types = study_types.join(",");
            var collection_id = $("#collection_id").val();

            formURL = $("#add_new_study_form").attr("action");
            csrftoken = $.cookie('csrftoken');

            $.ajax({
                url: formURL,
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                data: {'task':'add_new_study_types', 'collection_id': collection_id, 'study_types': study_types},
                success: function (data) {
                    location.reload();
                },
                error: function () {
                    alert("Couldn't add study types!");
                }
            });

        }
    }

})
