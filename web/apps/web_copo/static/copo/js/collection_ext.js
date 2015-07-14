$(document).ready(function () {

    //generate a tree view for cloning studies
    get_tree_data();


    $('[data-toggle="tooltip"]').tooltip();

    //handle event for date picker
    $('.pop_date_picker').datepick({
        dateFormat: 'D, M d, yyyy',
        altField: '#isoDate', altFormat: 'yyyy-mm-dd',
        showOnFocus: false,
        showTrigger: '<button type="button" class="trigger">...</button>'

    });

    //handle event for the submit button of add study type
    $("#submit_study_type_btn").click(function (event) {
        do_submit_study_type();
    });

    //hide delete button for first element in the study type group
    $("#study_type_remove_0").hide();

    //handle event for add new study type
    $('#btn_add_new_study_type').on('click', function () {
        do_add_new_study_type();
    });

    //handle event for add study type
    $("#study_type_add").click(function (event) {
        do_add_study_type();
    });

    //handle click event for delete study type
    $("#study_types_lists_div").on('click', 'a.study_type_remove', function (event) {
        do_remove_study_type(event);
    });


    //handle event for add new sample type
    $('#btn_add_new_study_sample').on('click', function () {
        do_add_new_study_sample();
    });

    //handle remove study sample
    $('.type_remove').on('click', function () {
        var the_action = this.id.split("/")[0];
        if (the_action == "remove_study_sample") {
            do_remove_study_sample(this.id);
        }
    });

    function do_clone_study_types() {
        var checkedNodes = $('#study_type_tree').tree('getChecked');
        for (var i = 0; i < checkedNodes.length; i++) {
            console.log(checkedNodes[i].id);
        }
    }


    function do_remove_study_sample(arg) {
        var study_samples_id = arg.split("/")[1];
        var collection_head_id = $("#collection_id").val();

        $.ajax({
            url: '/copo/remove_from_collection/',
            type: "GET",
            data: {
                'task': 'remove_study_sample',
                'collection_head_id': collection_head_id,
                'study_samples_id': study_samples_id
            },
            success: function (data) {
                location.reload();
            },
            error: function () {
                alert("Couldn't remove sample!");
            }
        });
    }

    function do_submit_study_type() {
        var $inputs = $('#add_new_study_form_2 :input');

        var form_values = {};
        $inputs.each(function () {
            var searchStr1 = "study_type_select_";
            var searchStr2 = "study_type_reference_";

            if (this.name.indexOf(searchStr1) > -1 || this.name.indexOf(searchStr2) > -1) {
                if(($(this).val()).trim() != "") {
                    form_values[this.name] = $(this).val();
                }
            }
        });

        var study_fields = JSON.stringify(form_values);

        var collection_head_id = $("#collection_head_id").val();


        formURL = $("#add_new_study_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_study',
                'collection_head_id': collection_head_id,
                'study_fields': study_fields
            },
            success: function (data) {
                display_new_study(data);
            },
            error: function () {
                alert("Couldn't add study!");
            }
        });

        //do_clone_study_types();

    }

    function display_new_study(data) {
        //clone an existing study as template for creating new ones

        var studies = data.ena_collection;
        for (var i = 0; i < studies.length; i++) {
            var clonableTarget = $(".study_table_row:last").clone();

            //update row id
            var targetId = clonableTarget.attr("id");
            var splitIndex = targetId.lastIndexOf("_");
            var literalPart = targetId.substr(0, splitIndex + 1);
            clonableTarget.attr("id", literalPart + studies[i].id);

            //update study_type_reference column
            var targetChild = clonableTarget.children(":nth-child(1)");
            var theRefTag = targetChild.children(":nth-child(1)");
            var splitLink = theRefTag.attr("href").split("/");
            theRefTag.attr("href", "/" + splitLink[1] + "/" + splitLink[2] + "/" + studies[i].id + "/" + splitLink[4]);
            theRefTag.html(studies[i].study_type_reference);

            //update the study_type column
            targetChild = clonableTarget.children(":nth-child(2)");
            targetChild.html(studies[i].study_type);

            //update the # samples column...maybe later

            //update the actions column
            targetChild = clonableTarget.children(":nth-child(4)");

            update_id_name_byref(targetChild.children(":nth-child(1)"), studies[i].id); //...for quick view study
            update_id_name_byref(targetChild.children(":nth-child(2)"), studies[i].id); //...for update study
            update_id_name_byref(targetChild.children(":nth-child(3)"), studies[i].id); //...for delete study


            $('.study_table_row:last').after(clonableTarget);

        }

        //refresh tree data
        get_tree_data();

        $('#newStudyTypeModal').modal('hide');
        $('.modal').on('hidden.bs.modal', function () {
            $(this).find('form')[0].reset();
        });

        //remove all redundant fields
        $('.study_type_remove').each(function () {
            var targetId = this.id;
            var splitIndex = targetId.lastIndexOf("_");
            var indexPart = targetId.substr(splitIndex + 1);

            if (parseInt(indexPart) > 0) {
                //remove study type object
                $("#study_type_select_divs_" + indexPart).remove();
            }

        });

    }

    function do_add_new_study_sample() { //need to attach bootstrap validator to form
        //using this to manage auto-generated fields
        var $inputs = $('#add_new_study_sample_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);


        //manage checkboxes
        var $candidates = $('input[name=assigned_study_type]:checked');
        var study_types = [];
        $candidates.each(function () {
            study_types[study_types.length] = $(this).val();
        });

        study_types = study_types.join(",");
        var collection_head_id = $("#collection_head_id").val();


        formURL = $("#add_new_study_sample_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_study_sample',
                'collection_head_id': collection_head_id,
                'study_types': study_types,
                'auto_fields': auto_fields
            },
            success: function (data) {
                location.reload();
            },
            error: function () {
                alert("Couldn't add samples!");
            }
        });
    }


    function do_add_new_study_type() {
        var $candidates = $('input[name=add_new_study_type]:checked');

        if ($candidates.length > 0) {
            var study_types = [];
            $candidates.each(function () {
                study_types[study_types.length] = $(this).val();
            });

            study_types = study_types.join(",");
            var collection_head_id = $("#collection_id").val();

            formURL = $("#add_new_study_form").attr("action");
            csrftoken = $.cookie('csrftoken');

            $.ajax({
                url: formURL,
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    'task': 'add_new_study_types',
                    'collection_head_id': collection_head_id,
                    'study_types': study_types
                },
                success: function (data) {
                    location.reload();
                },
                error: function () {
                    alert("Couldn't add study types!");
                }
            });

        }
    }

    function get_tree_data() {
        var collection_head_id = $("#collection_head_id").val();

        formURL = $("#add_new_study_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'get_tree_study',
                'collection_head_id': collection_head_id
            },
            success: function (data) {
                $('#study_type_tree').tree({
                    data: data.ena_studies
                });
            },
            error: function () {
                alert("Couldn't retrieve studies!");
            }
        });

    }

})
