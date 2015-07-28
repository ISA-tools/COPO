$(document).ready(function () {

    //do some housekeeping, encapsulates all dangling event declarations
    do_housekeeping();


    function do_housekeeping() {
        //generate a tree view for cloning studies
        refresh_study_tree_data();

        //...and for assigning sample to studies
        refresh_study_sample_tree_data();


        $('[data-toggle="tooltip"]').tooltip();

        //handle event for date picker
        $('.pop_date_picker').datepick({
            dateFormat: 'D, M d, yyyy',
            altField: '#isoDate', altFormat: 'yyyy-mm-dd',
            showOnFocus: false,
            showTrigger: '<button type="button" class="trigger">...</button>'

        });


        //hide delete button for first element in the study type group
        $("#study_type_remove_0").hide();

        //hide or show tables depending on presence of records to display
        if (parseInt($("#sample_data_count").val()) == 0) {
            $("#samples_table_div").hide();
        }

        if (parseInt($("#study_data_count").val()) == 0) {
            $("#studies_table_div").hide();
        }

        //handle event for add new study type
        $('#submit_study_type_btn').on('click', function () {
            do_submit_study_type();
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
        $('#btn_add_new_sample').on('click', function () {
            do_add_new_study_sample();
        });

        //handle edit sample
        $("#sample_table_div").on('click', 'a.sample_edit', function (event) {
            do_edit_sample(event);
        });

        $('.modal').on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $(this).find('form')[0].reset();

            if (this.id == "newStudyTypeModal") {
                do_disengage_study_modal();
            } else if (this.id == "newStudySampleModal") {
                do_disengage_sample_modal();
            }

        });

        //study tree events
        $('#study_type_tree').tree({
            onClick: function (node) {
                display_tree_info(node);
            },
            onCheck: function (node) {
                display_tree_info(node);
            }
        });
    }

    function display_tree_info(node) {
        var targetId = node.id;
        var splitIndex = targetId.lastIndexOf("_");
        var indexPart = targetId.substr(splitIndex + 1);

        if (indexPart == "leaf" || indexPart == "study") {
            $('#info_panel_display').parent().show();
            $('#info_panel_display').html(node.attributes.txt);

            if(indexPart == "leaf") {
                var elem = node.id+"_div"
                $("#"+elem).attr('class', 'study-tree-info-data-selected');
            }
        }

    }

    function do_edit_sample(event) {
        var sample_id = $($(event.target)).attr("id");

        //get actual sample id
        sample_id = sample_id.split("_")[1];

        var collection_head_id = $("#collection_head_id").val();

        formURL = $("#add_new_study_sample_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'get_study_sample',
                'collection_head_id': collection_head_id,
                'sample_id': sample_id
            },
            success: function (data) {
                display_sample_edit(data);
            },
            error: function () {
                alert("Couldn't retrieve sample!");
            }
        });
    }

    function display_sample_edit(data) {
        //todo: this mostly works for 'texty' kind of inputs. Will need to handle other types
        //todo: one way of doing that would be to check the tagName of the input, and deciding thence

        var sample = data.sample_data;
        var $inputs = $('#add_new_study_sample_form :input');

        $inputs.each(function () {
            var fieldId = this.id;
            var splitIndex = fieldId.lastIndexOf(".");
            var fieldTarget = fieldId.substr(splitIndex + 1);
            $(this).val(sample[fieldTarget]);
        });

        //hold the id of this sample for eventual persisting
        $('#current_sample_id').val(sample["id"]);

        //set the task too
        $('#current_sample_task').val("edit");

        //update tree view to show only unassigned studies
        $('#study_type_sample_tree').tree({
            data: data.ena_studies
        });
        $('#study_type_sample_tree').tree('expandAll');

        $('#newStudySampleModal').modal('show');

    }

    function do_get_tree_checked(tree_id) {
        var checkedNodes = $("#" + tree_id).tree('getChecked');
        return checkedNodes;
    }


    function do_submit_study_type() {
        var $inputs = $('#add_new_study_form_2 :input');

        var form_values = {};
        $inputs.each(function () {
            var searchStr1 = "study_type_select_";
            var searchStr2 = "study_type_reference_";

            if (this.name.indexOf(searchStr1) > -1 || this.name.indexOf(searchStr2) > -1) {
                if (($(this).val()).trim() != "") {
                    form_values[this.name] = $(this).val();
                }
            }
        });

        var study_fields = JSON.stringify(form_values);
        var collection_head_id = $("#collection_head_id").val();

        // handle cloned studies
        var selectedNodes = do_get_tree_checked("study_type_tree");

        var allStudyIds = [];
        var allStudyFragments = [];
        var splitIndex;
        var studyId;

        for (var i = 0; i < selectedNodes.length; i++) {
            splitIndex = selectedNodes[i].id.indexOf("_");
            studyId = selectedNodes[i].id.substr(0, splitIndex);
            allStudyIds[i] = studyId;
            allStudyFragments[i] = selectedNodes[i].id;
        }

        //get unique studies
        var uniqueStudyIds = allStudyIds.filter(function (item, i, ar) {
            return ar.indexOf(item) === i;
        });

        //retrieve study fragments
        var clonedStudies = [];
        for (var i = 0; i < uniqueStudyIds.length; i++) {
            var curId = uniqueStudyIds[i];


            var study_fragments = {"study_id": curId};

            //get study_type
            study_fragments["study_type"] = "false";
            if ($.inArray(curId + "_study_type_leaf", allStudyFragments) > -1) {
                study_fragments["study_type"] = "true";
            }

            var samples = [];
            var contacts = [];
            var publications = [];

            for (var j = 0; j < allStudyFragments.length; j++) {
                var curNode = allStudyFragments[j];
                var studyIdPart = curNode.substring(0, curNode.indexOf('_'));

                if (curId != studyIdPart) {
                    continue;
                }

                //samples
                if (curNode.substr(curNode.length - 12) == "_sample_leaf") {
                    samples[samples.length] = curNode.split("_")[1];
                }

                //contacts
                if (curNode.substr(curNode.length - 13) == "_contact_leaf") {
                    contacts[contacts.length] = curNode.split("_")[1];
                }

                //publications
                if (curNode.substr(curNode.length - 17) == "_publication_leaf") {
                    publications[publications.length] = curNode.split("_")[1];
                }


            }

            study_fragments["samples"] = samples.join();
            study_fragments["contacts"] = contacts.join();
            study_fragments["publications"] = publications.join();

            clonedStudies[i] = study_fragments;

        }

        var cloned_studies = JSON.stringify(clonedStudies);


        formURL = $("#add_new_study_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_study',
                'collection_head_id': collection_head_id,
                'study_fields': study_fields,
                'cloned_studies': cloned_studies
            },
            success: function (data) {
                display_new_study(data);
            },
            error: function () {
                alert("Couldn't add study!");
            }
        });

    }

    function display_new_sample(data) {
        $('#newStudySampleModal').modal('hide');

        //refresh the sample table
        $('#sample_table_div').html(data.sample_data);

        //also refresh the study table
        display_new_study(data);
    }

    function display_new_study(data) {
        //clone an existing study as template for minting new ones

        var studies = data.study_data;

        var clonedTR = [];
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
            theRefTag.html(studies[i].studyReference);

            //update the study_type column
            targetChild = clonableTarget.children(":nth-child(2)");
            targetChild.html(studies[i].studyType);

            //update the # samples column
            targetChild = clonableTarget.children(":nth-child(3)");
            targetChild.html(studies[i].samplescount);

            //update the actions column
            targetChild = clonableTarget.children(":nth-child(4)");

            update_id_name_byref(targetChild.children(":nth-child(1)"), studies[i].id); //...for quick view study
            update_id_name_byref(targetChild.children(":nth-child(2)"), studies[i].id); //...for update study
            update_id_name_byref(targetChild.children(":nth-child(3)"), studies[i].id); //...for delete study

            clonedTR[i] = clonableTarget;

        }

        $("#study_table").find("tr:gt(0)").remove();

        for (var i = 0; i < clonedTR.length; i++) {
            $('#study_table').append(clonedTR[i]);
        }

        //refresh tree data
        refresh_study_tree_data();

        //also refresh tree in sample modal
        refresh_study_sample_tree_data();

        $('#newStudyTypeModal').modal('hide');

        do_disengage_study_modal();

    }

    function do_disengage_sample_modal() {
        $('#current_sample_id').val("");
        $('#current_sample_task').val("");
        refresh_study_sample_tree_data();
    }

    function do_disengage_study_modal() {

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

    function do_add_new_study_sample() { //todo: attached bootstrap validator
        //manage auto-generated fields
        var $inputs = $('#add_new_study_sample_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);

        var selectedStudies = do_get_tree_checked("study_type_sample_tree");
        var study_types = [];

        for (var i = 0; i < selectedStudies.length; i++) {
            study_types[i] = selectedStudies[i].id;
        }

        study_types = study_types.join(",");


        var collection_head_id = $("#collection_head_id").val();

        var sample_id = ""
        var task = "add_new_study_sample"
        if ($("#current_sample_task").val() == "edit") {
            task = "edit_study_sample";
            sample_id = $("#current_sample_id").val();
        }


        formURL = $("#add_new_study_sample_form").attr("action");
        csrftoken = $.cookie('csrftoken');


        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': task,
                'collection_head_id': collection_head_id,
                'study_types': study_types,
                'auto_fields': auto_fields,
                'sample_id': sample_id
            },
            success: function (data) {
                display_new_sample(data);
            },
            error: function () {
                alert("Couldn't add sample!");
            }
        });
    }

    function refresh_study_tree_data() {
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

    function refresh_study_sample_tree_data() {
        var collection_head_id = $("#collection_head_id").val();

        formURL = $("#add_new_study_sample_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'get_tree_study_sample',
                'collection_head_id': collection_head_id
            },
            success: function (data) {
                $('#study_type_sample_tree').tree({
                    data: data.ena_studies
                });
                $('#study_type_sample_tree').tree('expandAll');
            },
            error: function () {
                alert("Couldn't retrieve studies data!");
            }
        });

    }


})
