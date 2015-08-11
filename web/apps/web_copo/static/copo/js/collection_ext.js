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

        //disable submit in clone study
        $("#submit_study_clone_btn").prop('disabled', true);

        //hide delete button for first element in the study type group
        $("#study_type_remove_0").hide();

        //handle event for add new study type
        $('#submit_study_type_btn').on('click', function () {
            do_submit_study_type();
        });

        //handle event for delete study confirmation
        $('#delete_study_btn').on('click', function () {
            do_delete_study();
        });

        //handle event for clone study
        $('#submit_study_clone_btn').on('click', function () {
            do_clone_study();
        });


        //handle event for add study type
        $(".study-type-add").click(function (event) {
            do_add_study_type();
        });

        //handle click event for delete study type
        $("#study_types_lists_div").on('click', 'a.study-type-remove', function (event) {
            do_remove_study_type(event);
        });

        //handle event for delete study
        $("#studies_table_div").on('click', 'a.study-delete', function (event) {
            do_study_delete_confirmation(event);
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

            try {
                $(this).find('form')[0].reset();
            } catch (err) {
                ;
            }

            if (this.id == "newStudyTypeModal") {
                do_disengage_study_modal();
            } else if (this.id == "newStudySampleModal") {
                do_disengage_sample_modal();
            } else if (this.id == "studyTypeCloneModal") {
                do_disengage_study_clone_modal();
            } else if (this.id == "studyDeleteModal") {
                do_disengage_study_delete_modal();
            }

        });

        //study tree events
        $('#study_type_tree').tree({
            onClick: function (node) {
                display_tree_info(node);
            },
            onCheck: function (node, checked) {
                display_tree_node_status(node, checked);
                refresh_study_clone_info();
            }
        });
    }

    function do_delete_study() {
        //get the study id...
        var studyId = $("#target_study_delete").val();

        var collection_head_id = $("#collection_head_id").val();

        formURL = $("#delete_study_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'delete_study',
                'collection_head_id': collection_head_id,
                'study_id': studyId
            },
            success: function (data) {
                display_new_study(data);
                $('#studyDeleteModal').modal('hide');
                do_disengage_study_delete_modal();
            },
            error: function () {
                alert("Couldn't add new study!");
            }
        });

    }

    function do_study_delete_confirmation(event) {
        var targetId = $($(event.target)).parent().attr("id");
        var studyRef = $($(event.target)).parent().attr("custom-data-reference");
        var studyType = $($(event.target)).parent().attr("custom-data-type");

        if (targetId.slice(-9) == "st_delete") {
            studyId = targetId.slice(0, -10);
            studyRow = studyId + "_study_row";

            $("#" + studyRow).attr('class', 'row-delete-higlight');
            $("#target_study_delete_span").html(studyRef + " (" + studyType + ")");
            $("#target_study_delete").val(studyId);
        }
    }

    function display_tree_node_status(node, checked) {
        //first display the study branch...

        $('#info_panel_display').show();

        //handle checked nodes,
        //nodes at the same level across studies are mutually exclusive
        var selectedNodes = do_get_tree_checked("study_type_tree");
        if (checked) {
            $("#cloned_panel_display").show();

            for (var i = 0; i < selectedNodes.length; i++) {

                if (node.id == selectedNodes[i].id) {
                    continue;
                }

                targetSplit = node.id.split("_");
                elemSplit = selectedNodes[i].id.split("_");


                if ((targetSplit.length == 2
                    && elemSplit.length == 2)
                    && (targetSplit[1] == elemSplit[1])) {
                    elemNode = $('#study_type_tree').tree('find', selectedNodes[i].id);
                    $('#study_type_tree').tree('uncheck', elemNode.target);
                } else if ((targetSplit.length == 3
                    && elemSplit.length == 3)
                    && (targetSplit[1] + targetSplit[2] == elemSplit[1] + elemSplit[2])) {
                    elemNode = $('#study_type_tree').tree('find', selectedNodes[i].id);
                    $('#study_type_tree').tree('uncheck', elemNode.target);
                }
            }
        }

        // display the branch of this node in the view pane
        var display_txt = node.attributes.txt;
        if (display_txt == "") {
            var rootNode = $('#study_type_tree').tree('find', node.id.substring(0, node.id.indexOf('_')) + "_study");
            display_txt = rootNode.attributes.txt;
        }

        $('#info_panel_display').html(display_txt);
    }

    function refresh_study_clone_info() {
        var selectedNodes = do_get_tree_checked("study_type_tree");

        //update the view in the cloned pane
        //hide all node by default...show selected elements
        $("#cloned_panel_display").children(":nth-child(1)").children().each(function () {
            if ($("#" + this.id).get(0) && (this.id.slice(-9) == "clone_div")) {
                $("#" + this.id).hide();
            }
        });

        //clear composite-type nodes ready for rebuilding
        $(".study-list-data-active").remove();

        //show all passive divs
        //passive divs are used to clone composite nodes
        $(".study-list-data-passive").show();

        for (var i = 0; i < selectedNodes.length; i++) {
            elemSplit = selectedNodes[i].id.split("_");
            literalPart = elemSplit[elemSplit.length - 1]

            elemDiv = literalPart + "_clone_div";

            if ($("#" + elemDiv).get(0)) {
                $("#" + elemDiv).show();

                //set values...but done in a slightly different way depending on the level of nesting of nodes
                if (elemSplit.length == 2) {
                    elemSpan = literalPart + "_clone_span";
                    $("#" + elemSpan).html(selectedNodes[i].attributes.label);

                    elemValue = literalPart + "_clone_value";
                    $("#" + elemValue).val(selectedNodes[i].attributes.value);
                } else if (elemSplit.length == 3) {
                    //find and retrieve the composite node data
                    elemNode = $('#study_type_tree').tree('find', selectedNodes[i].id);
                    dataDivs = elemNode.attributes.label;

                    clonableDiv = $("#" + elemDiv).find(".study-list-data-passive").clone();
                    clonableDiv.attr("class", "study-list-data-active");
                    clonableDiv.find(".study-node-data").html(dataDivs);
                    clonableDiv.find(".study-node-data-value").attr("id", literalPart + "_" + i + "_clone_value");
                    clonableDiv.find(".study-node-data-value").val(elemNode.attributes.value);
                    $("#" + elemDiv).append(clonableDiv);

                }
            }
        }

        //hide all passive divs
        $(".study-list-data-passive").hide();

        //check if minimum requirement for cloning is met before activating the submit button
        // ...i.e. do some validation here!
        if (selectedNodes.length > 0) {
            $("#submit_study_clone_btn").prop('disabled', false);
        } else {
            $("#submit_study_clone_btn").prop('disabled', true);
        }
    }

    function display_tree_info(node) {
        var targetId = node.id;

        $('#info_panel_display').show();

        var display_txt = node.attributes.txt;
        if (display_txt == "") {
            var rootNode = $('#study_type_tree').tree('find', targetId.substring(0, targetId.indexOf('_')) + "_study");
            display_txt = rootNode.attributes.txt;
        }

        $('#info_panel_display').html(display_txt);

        var elem = node.id + "_div"

        if ($("#" + elem).get(0)) { // change class to highlighted
            $("#" + elem).attr('class', 'study-tree-info-data-selected');
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

    function do_clone_study() {
        var $inputs = $('#clone_new_study_form_2 :input');

        var form_values = {};

        $inputs.each(function () {
            if (this.id.slice(-11) == "clone_value") {
                form_values[this.id.slice(0, -12)] = $(this).val();
            }
        });

        var cloned_elements = JSON.stringify(form_values);
        var collection_head_id = $("#collection_head_id").val();

        formURL = $("#clone_new_study_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'clone_study',
                'collection_head_id': collection_head_id,
                'cloned_elements': cloned_elements
            },
            success: function (data) {
                display_new_study(data);
                $('#studyTypeCloneModal').modal('hide');
                do_disengage_study_clone_modal();
            },
            error: function () {
                alert("Couldn't clone study!");
            }
        });

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
                $('#newStudyTypeModal').modal('hide');
                do_disengage_study_modal();
            },
            error: function () {
                alert("Couldn't add new study!");
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

       $('#studies_table_div').html(data.study_data);

        //refresh tree data
        refresh_study_tree_data();

        //also refresh tree in sample modal
        refresh_study_sample_tree_data();
    }

    function do_disengage_study_clone_modal() {
        refresh_study_tree_data();
        $('#info_panel_display').html("");
        $("#cloned_panel_display").hide();
        $('#studyReference_clone_value').val("");
        $("#submit_study_clone_btn").prop('disabled', true);
    }

    function do_disengage_sample_modal() {
        $('#current_sample_id').val("");
        $('#current_sample_task').val("");
        refresh_study_sample_tree_data();
    }

    function do_disengage_study_modal() {

        //remove all redundant fields
        $('.study-type-remove').each(function () {
            var targetId = this.id;
            var splitIndex = targetId.lastIndexOf("_");
            var indexPart = targetId.substr(splitIndex + 1);

            if (parseInt(indexPart) > 0) {
                //remove study type object
                $("#study_type_select_divs_" + indexPart).remove();
            }

        });

    }

    function do_disengage_study_delete_modal() {
        //get the study id...
        var studyId = $("#target_study_delete").val();
        var studyRow = studyId + "_study_row";

        $("#" + studyRow).removeClass("row-delete-higlight");
        $("#target_study_delete_span").html("");
        $("#target_study_delete").val("");
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
