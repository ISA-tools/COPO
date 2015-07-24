$(document).ready(function () {

    //do some housekeeping, encapsulates all dangling event declarations
    do_housekeeping();


    function do_housekeeping() {
        do_populate_details_fields();

        //handle event for date picker
        $('.pop_date_picker').datepick({
            dateFormat: 'D, M d, yyyy',
            altField: '#isoDate', altFormat: 'yyyy-mm-dd',
            showOnFocus: false,
            showTrigger: '<button type="button" class="trigger">...</button>'

        });


        $('#study_reference_qupdate').on('click', function () {
            $('#show_quick_ref_update').toggle();
        });

        //handle study type / study reference event
        $('#btn_study_type_quick_update').on('click', function () {
            do_study_type_quick_update();
        });

        //handle study details update
        $('#btn_update_study_details').on('click', function () {
            do_study_details_update();
        });

        //handle event for hiding alert boxes
        $("[data-hide]").on("click", function () {
            $(this).closest("." + $(this).attr("data-hide")).hide();
        });
    }

    function do_populate_details_fields() {
        var ena_collection_id = $("#ena_collection_id").val();
        var study_id = $("#study_id").val();

        formURL = $("#study_details_update_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'get_study_data',
                'ena_collection_id': ena_collection_id,
                'study_id': study_id
            },
            success: function (data) {
                display_study_details(data);
            },
            error: function () {
                alert("Couldn't get study details!");
            }
        });
    }

    function display_study_details(data) {
        //todo: this mostly works for 'texty' kind of inputs. Will need to handle other types
        //todo: one way of doing that would be to check the tagName of the input, and deciding thence

        var study = data.study_data;
        var $inputs = $('#study_details_update_form :input');

        $inputs.each(function () {
            var fieldId = this.id;
            var splitIndex = fieldId.lastIndexOf(".");
            var fieldTarget = fieldId.substr(splitIndex + 1);
            $(this).val(study[fieldTarget]);
        });

    }

    function do_study_details_update() {
        //manage auto-generated fields
        var $inputs = $('#study_details_update_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);

        var ena_collection_id = $("#ena_collection_id").val();
        var study_id = $("#study_id").val();

        $("#btn_update_study_details").hide();
        $("#study_details_update_img").show();

        formURL = $("#study_details_update_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'update_study_details',
                'ena_collection_id': ena_collection_id,
                'study_id': study_id,
                'auto_fields': auto_fields
            },
            success: function (data) {
                display_updated_study_details(data);
            },
            error: function () {
                alert("Couldn't update study details!");
            }
        });
    }

    function display_updated_study_details(data) {
        setTimeout(function () {
            display_study_details(data);

            $("#btn_update_study_details").show();
            $("#study_details_update_img").hide();
        }, 400);
    }


    function do_study_type_quick_update() {
        //only initiate update if values have changed

        //get currently displayed values
        var study_type = $("#study_type").val();
        var study_type_reference = $("#study_type_reference").val();

        //get updated values
        var new_study_type = $("#study_type_quick_update").val();
        var new_study_type_reference = $("#study_reference_quick_update").val();

        var ena_collection_id = $("#ena_collection_id").val();
        var study_id = $("#study_id").val();

        if ((study_type != new_study_type) || (study_type_reference != new_study_type_reference)) {
            $("#btn_study_type_quick_update").hide();
            $("#study_type_qupdate_img").show();

            formURL = $("#study_type_qupdate_form").attr("action");
            csrftoken = $.cookie('csrftoken');

            $.ajax({
                url: formURL,
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    'task': 'update_study_type',
                    'ena_collection_id': ena_collection_id,
                    'study_id': study_id,
                    'study_type': new_study_type,
                    'study_type_reference': new_study_type_reference
                },
                success: function (data) {
                    display_new_study_type(data);
                },
                error: function () {
                    alert("Couldn't update study type!");
                }
            });
        }

    }

    function display_new_study_type(data) {
        setTimeout(function () {
            $("#study_type_span").html(data.study_type_data["study_type_label"]);
            $("#study_reference_type_span").html(data.study_type_data["study_type_reference"]);

            $("#study_type").val(data.study_type_data["study_type"]);
            $("#study_type_reference").val(data.study_type_data["study_type_reference"]);

            $("#study_type_quick_update").val(data.study_type_data["study_type"]);

            $("#btn_study_type_quick_update").show();
            $("#study_type_qupdate_img").hide();
        }, 400);

    }


})
