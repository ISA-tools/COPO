$(document).ready(function () {

    //do some housekeeping, encapsulates all dangling event declarations
    do_housekeeping();

    function do_housekeeping() {

        refresh_tool_tips();

        //will populate form fields
        do_populate_details_fields();

        //refresh selectbox
        refresh_selectbox();


        //handle event for study samples table refresh under
        $(".study-samples-refresh-modal").click(function (event) {
            refresh_sample_tree_data();

            //...just in case the samples assignment warning is still on
            if ($("#sample_assignment_warning").get(0)) {
                $("#sample_assignment_warning").hide();
            }

        });

        //handle event for date picker
        $('.pop_date_picker').datepick({
            dateFormat: 'D, M d, yyyy',
            altField: '#isoDate', altFormat: 'yyyy-mm-dd',
            showOnFocus: false,
            showTrigger: '<button type="button" class="trigger">...</button>'

        });

        //handle event for when new datafile addition
        $('#new_data_file_id').on('change', function () {
            //refresh for dynamic bindings
            refresh_selectbox();
            refresh_tool_tips();
        });

        //handles event to show/hide study reference/type form
        $('#study_reference_qupdate').on('click', function () {
            $('#show_quick_ref_update').toggle();
        });

        //handle study type / study reference event
        $('#btn_study_type_quick_update').on('click', function () {
            do_study_type_quick_update();
        });

        //handle publication doi resolve event
        $('#btn_publication_doi_resolve').on('click', function () {
            do_publication_doi();
        });

        //handle check all
        $("#sample_tree_table").on('click', 'input.check-pointer', function (event) {
            do_check_all(event);
        });

        //handle event to add new publication
        $('#btn_add_new_publication').on('click', function () {
            do_add_publication();
        });

        //handle event to add new protocol
        $('#btn_add_new_protocol').on('click', function () {
            do_add_protocol();
        });


        //handle event to add new contact
        $('#btn_add_new_contact').on('click', function () {
            do_add_contact();
        });

        //handle study details update
        $('#btn_update_study_details').on('click', function () {
            do_study_details_update();
        });

        //handle event for assigning samples
        $('#submit_sample_assign_btn').on('click', function () {
            do_assign_samples_to_study();
        });

        //handle event for component row delete
        $(document).on("click", ".component-row-delete", function (event) {
            //implements bootstrap-dialog for components delete
            do_component_delete_confirmation(event);
        });


        //handle show file attributes
        $("#study_data_table_div").on('click', 'a.data-file-attribute', function (event) {
            event.preventDefault();
        });


        //spin up sample description
        $("#study_samples_table_div").on('click', 'a.sample-describe', function (event) {
            do_describe_sample(event);
        });


        //handle event for delete tasks proceeding from studyComponentsDeleteModal
        $('#delete_task_btn').on('click', function () {
            dispatch_delete_task();
        });

        //handle sample assignment checkbox event
        $("#sample_tree_table").on('click', 'input.check-pointer', function (event) {
            if ($($(event.target)).attr('name') == "study_samples_assign_chk") {
                do_samples_assign_warning();
            }
        });

        //handle modal hide events
        $('.modal').on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();

            try {
                $(this).find('form')[0].reset();
            } catch (err) {
                ;
            }

            if (this.id == "studyComponentsDeleteModal") {
                do_disengage_studyComponentsDeleteModal();
            }

        });

    }

    function do_check_all(event) {
        var theObj = $($(event.target));

        if ((typeof theObj.attr("name") !== "undefined")) {

            if (theObj.attr("id") == "assign_samples_study") {
                if (theObj.is(':checked')) {
                    $("input[name='study_samples_assign_chk']").each(function () {
                        this.checked = true;
                    });
                } else {
                    $("input[name='study_samples_assign_chk']").each(function () {
                        this.checked = false;
                    });
                }
            } else if (theObj.attr("name") == "study_samples_assign_chk") {
                //if at least one is unchecked, uncheck the "check all" button, vice-versa
                var checkedr = true;
                $("input[name='study_samples_assign_chk']").each(function () {
                    if (!this.checked) {
                        checkedr = false;
                        return;
                    }
                });

                if (!checkedr) {
                    $('#assign_samples_study').prop('checked', false);
                }
            }

            do_samples_assign_warning();
        }
    }

    function do_attach_samples_to_file(value) {
        var samples = [];

        value.forEach(function (item) {
            var item = item.split(",")
            dataFileId = item[0];
            samples.push(item[1]);
        });

        var samples = JSON.stringify(samples);

        //spin off a request to update samples

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#study_details_update_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'attach_file_sample',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'samples': samples,
                'data_file_id': dataFileId
            },
            success: function (data) {
                $("#study_data_table_div").html(data.data_file_html);
                refresh_selectbox();
                refresh_tool_tips();
            },
            error: function () {
                alert("Couldn't attach Samples to File!");
            }
        });

    }

    function do_describe_sample(event) {
        var targetId = $($(event.target)).attr("id");

        var literalPart = "sample_describe";

        if (typeof targetId !== "undefined") {
            if (targetId.slice(-(parseInt(literalPart.length))) == literalPart) {

                sampleId = targetId.slice(0, -(parseInt(literalPart.length + 1)));


                var ena_collection_id = $("#ena_collection_id").val();
                var studyId = $("#study_id").val();

                formURL = $("#sample_description_form").attr("action");
                csrftoken = $.cookie('csrftoken');

                $.ajax({
                    url: formURL,
                    type: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        'task': 'get_study_sample',
                        'ena_collection_id': ena_collection_id,
                        'study_id': studyId,
                        'sample_id': sampleId
                    },
                    success: function (data) {
                        $("#sample_description_name").html(data.sample_data.sampleName);
                    },
                    error: function () {
                        alert("Couldn't resolve Sample details!");
                    }
                });

            }
        }
    }

    function do_component_delete_confirmation(event) {
        var elem = $($(event.target)).parent();

        var targetId = elem.attr("target-id");
        var targetComponentMessage = elem.attr("component-message");
        var targetComponentTitle = elem.attr("component-title");

        var code = BootstrapDialog.show({
            type: BootstrapDialog.TYPE_DANGER,
            title: $(elem.find('.themess').html()),
            message: $(targetComponentMessage),
            buttons: [
                {
                    label: 'Cancel',
                    action: function (dialogItself) {
                        dialogItself.close();
                    }
                },
                {
                    icon: 'glyphicon glyphicon-trash',
                    label: 'Delete',
                    cssClass: 'btn-danger',
                    action: function () {
                        alert('No!!!!!');
                    }
                }
            ]
        });


        //$("#delete_component").html(targetTitle);
        //$("#delete_component_message").html(targetTitle);
        //
        //var elem = $("#" + targetId + "_" + targetComponent + "_row");
        //
        //if (elem) {
        //    elem.attr('class', 'row-delete-higlight');
        //    $("#target_delete_id").val(targetId);
        //    $("#target_delete_component").val(targetComponent);
        //}

    }


    function do_publication_doi() {
        var doiHandle = $("#publication_doi").val();

        doiHandle = doiHandle.replace(/^\s+|\s+$/g, '');

        if (doiHandle.length == 0) {
            return false;
        }

        $("#btn_publication_doi_resolve").hide();
        $("#publication_doi_img").show();

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#publication_doi_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'resolve_publication_doi',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'doi_handle': doiHandle
            },
            success: function (data) {
                display_doi_publication(data);
            },
            error: function () {
                alert("Couldn't resolve DOI!");
            }
        });
    }

    function display_doi_publication(data) {
        if (data.publication_doi_data.status == "success") {
            var publication_doi_data = data.publication_doi_data.data;
            var publication_fields_mappings = data.ena_fields_mapping;
            var $inputs = $('#add_new_publication_form :input');

            $inputs.each(function () {
                var fieldId = this.id;
                var splitIndex = fieldId.lastIndexOf(".");
                var fieldTarget = fieldId.substr(splitIndex + 1);
                fieldTarget = publication_fields_mappings[fieldTarget];
                $(this).val(publication_doi_data[fieldTarget]);
            });
        }

        $("#btn_publication_doi_resolve").show();
        $("#publication_doi_img").hide();
        $("#publication_doi").val("");
        $('#publicationAddModal').modal('show');
    }

    function do_add_protocol() {
        //manage auto-generated fields
        var $inputs = $('#add_new_protocol_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);


        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#add_new_protocol_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_protocol',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'auto_fields': auto_fields
            },
            success: function (data) {
                refresh_table_data(data, "protocols");
            },
            error: function () {
                alert("Couldn't retrieve protocols!");
            }
        });
    }

    function do_add_publication() {
        //manage auto-generated fields
        var $inputs = $('#add_new_publication_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);


        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#add_new_publication_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_publication',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'auto_fields': auto_fields
            },
            success: function (data) {
                refresh_table_data(data, "publications");
            },
            error: function () {
                alert("Couldn't retrieve publications!");
            }
        });
    }

    function do_add_contact() {
        //manage auto-generated fields
        var $inputs = $('#add_new_contact_form :input');

        var form_values = {};
        $inputs.each(function () {
            form_values[this.name] = $(this).val();
        });

        var auto_fields = JSON.stringify(form_values);


        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#add_new_contact_form").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'add_new_contact',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'auto_fields': auto_fields
            },
            success: function (data) {
                refresh_table_data(data, "contacts");
            },
            error: function () {
                alert("Couldn't retrieve contacts!");
            }
        });
    }

    function do_assign_samples_to_study() {
        //get samples status
        var samples_status = do_samples_assign_warning();

        //get assigned samples
        var selected_study_samples = samples_status["selected_study_samples"].join(",");

        //get excluded ones for deletion
        var excluded_study_samples = samples_status["excluded_study_samples"].join(",");

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#assign_sample_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'assign_samples_to_study',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'selected_study_samples': selected_study_samples,
                'excluded_study_samples': excluded_study_samples
            },
            success: function (data) {
                refresh_table_data(data, "samples");
                refresh_table_data(data, "datafiles");

            },
            error: function () {
                alert("Couldn't retrieve samples!");
            }
        });
    }

    function do_samples_assign_warning() {
        //get assigned samples
        var selected_study_samples = [];
        $("input[name=study_samples_assign_chk]:checked:enabled").each(function () {
            selected_study_samples.push($(this).val());
        });

        //get all existing samples, and un-highlight
        var existing_study_samples = [];
        $("tr[id$='sample_row']").each(function () {
            existingSampleId = this.id.slice(0, -11);
            existing_study_samples.push(existingSampleId);
            $("#" + existingSampleId + "_sample_assignment_row").removeClass("row-delete-higlight");
        });

        $("#sample_assignment_warning").hide();


        var excluded_study_samples = [];
        existing_study_samples.forEach(function (entry) {
            if ($.inArray(entry, selected_study_samples) < 0) {
                $("#" + entry + "_sample_assignment_row").attr('class', 'row-delete-higlight');
                excluded_study_samples.push(entry);
            }
        });

        if (excluded_study_samples.length > 0) {
            $("#sample_assignment_warning").show();
        }

        //for some re-using
        var samples_status = {};
        samples_status["selected_study_samples"] = selected_study_samples;
        samples_status["excluded_study_samples"] = excluded_study_samples;

        return samples_status;

    }

    function refresh_sample_tree_data() {
        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#assign_sample_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'get_tree_samples_4_studies',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId
            },
            success: function (data) {
                $('#sample_tree_table').html(data.samples_tree);
            },
            error: function () {
                alert("Couldn't retrieve samples!");
            }
        });

    }

    function do_delete_sample(id) {
        var sampleId = id;

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#delete_element_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'delete_sample_from_study',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'sample_id': sampleId
            },
            success: function (data) {
                refresh_table_data(data, "samples");
                refresh_table_data(data, "datafiles");
            },
            error: function () {
                alert("Couldn't delete sample!");
            }
        });
    }

    function do_delete_datafile(id) {
        var dataFileId = id;

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#delete_element_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'delete_datafile_from_study',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'data_file_id': dataFileId
            },
            success: function (data) {
                refresh_table_data(data, "datafiles");
            },
            error: function () {
                alert("Couldn't delete sample!");
            }
        });
    }

    function do_delete_publication(id) {
        var publicationId = id;

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#delete_element_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'delete_publication_from_study',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'publication_id': publicationId
            },
            success: function (data) {
                refresh_table_data(data, "publications");
            },
            error: function () {
                alert("Couldn't delete publication!");
            }
        });
    }

    function do_delete_contact(id) {
        var contactId = id;

        var ena_collection_id = $("#ena_collection_id").val();
        var studyId = $("#study_id").val();

        formURL = $("#delete_element_form_2").attr("action");
        csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: formURL,
            type: "POST",
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'task': 'delete_contact_from_study',
                'ena_collection_id': ena_collection_id,
                'study_id': studyId,
                'contact_id': contactId
            },
            success: function (data) {
                refresh_table_data(data, "contacts");
            },
            error: function () {
                alert("Couldn't delete contact!");
            }
        });
    }


    function refresh_table_data(data, component) {
        if (component == "samples") {
            $('#study_samples_table_div').html(data.sample_data);

            $('#samplesAssignModal').modal('hide');
        } else if (component == "publications") {
            $('#study_publications_table_div').html(data.publication_data);

            //hide modals associated with component
            $('#publicationAddModal').modal('hide');
        } else if (component == "contacts") {
            $('#study_contacts_table_div').html(data.contact_data);

            $('#contactAddModal').modal('hide');
        } else if (component == "datafiles") {
            //refresh datafiles table
            $("#study_data_table_div").html(data.data_file_html);
            refresh_selectbox(); //to bind dynamic fields
        }

        refresh_tool_tips();
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

    function do_disengage_studyComponentsDeleteModal() {
        var targetId = $("#target_delete_id").val();
        var targetComponent = $("#target_delete_component").val();

        var elem = $("#" + targetId + "_" + targetComponent + "_row");

        if (elem) {
            elem.removeClass('row-delete-higlight');
            $("#target_delete_id").val("");
            $("#target_delete_component").val("");

            $("#delete_component").html("");
            $("#delete_component_message").html("");
        }

        $('#studyComponentsDeleteModal').modal('hide');

        refresh_tool_tips();
    }

    function dispatch_delete_task() {
        var targetId = $("#target_delete_id").val();
        var targetComponent = $("#target_delete_component").val();

        if (targetComponent == "sample") {
            do_delete_sample(targetId);
        } else if (targetComponent == "publication") {
            do_delete_publication(targetId);
        } else if (targetComponent == "contact") {
            do_delete_contact(targetId);
        } else if (targetComponent == "datafile") {
            do_delete_datafile(targetId);
        }

        do_disengage_studyComponentsDeleteModal();

    }

    //refreshes selectboxes to pick up events

    function refresh_selectbox() {
        //file-sample selectbox
        $('.file-sample-select').selectize({
            onChange: function (value) {
                if (value) {
                    do_attach_samples_to_file(value);
                }

            },
            dropdownParent: 'body',
            maxItems: 'null',
            plugins: ['remove_button']
        });
    }


})
