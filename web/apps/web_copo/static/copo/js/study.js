$(document).ready(function () {

        //do some housekeeping, encapsulates all dangling event declarations
        do_housekeeping();

        function do_housekeeping() {

            $("#grid-basic").bootgrid();

            $("#example-basic").steps({
                headerTag: "h3",
                bodyTag: "section",
                transitionEffect: "slideLeft",
                autoFocus: true,
                stepsOrientation: "vertical"
            });


            refresh_tool_tips();

            //will populate form fields
            do_populate_details_fields();

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

            //handle event for sample delete
            $("#study_samples_table_div").on('click', 'a.sample-delete', function (event) {
                do_sample_delete_confirmation(event);
            });

            //spin up sample description
            $("#study_samples_table_div").on('click', 'a.sample-describe', function (event) {
                do_describe_sample(event);
            });

            //handle event for publication delete
            $("#study_publications_table_div").on('click', 'a.publication-delete', function (event) {
                do_publication_delete_confirmation(event);
            });

            //handle event for contact delete
            $("#study_contacts_table_div").on('click', 'a.contact-delete', function (event) {
                do_contact_delete_confirmation(event);
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

        function do_publication_delete_confirmation(event) {
            var targetId = $($(event.target)).attr("id");

            $("#delete_component").html(" Publication ");
            $("#delete_component_message").html(" publication");


            var literalPart = "publication_delete";
            var rowLiteralPart = "_publication_row";

            if (typeof targetId !== "undefined") {
                if (targetId.slice(-(parseInt(literalPart.length))) == literalPart) {
                    elementId = targetId.slice(0, -(parseInt(literalPart.length + 1)));
                    elementRow = elementId + rowLiteralPart;

                    $("#target_delete_id").val(elementId + "_publication");
                    $("#" + elementRow).attr('class', 'row-delete-higlight');

                }
            }
        }

        function do_contact_delete_confirmation(event) {
            var targetId = $($(event.target)).attr("id");

            $("#delete_component").html(" Contact ");
            $("#delete_component_message").html(" contact");


            var literalPart = "contact_delete";
            var rowLiteralPart = "_contact_row";

            if (typeof targetId !== "undefined") {
                if (targetId.slice(-(parseInt(literalPart.length))) == literalPart) {
                    elementId = targetId.slice(0, -(parseInt(literalPart.length + 1)));
                    elementRow = elementId + rowLiteralPart;

                    $("#target_delete_id").val(elementId + "_contact");
                    $("#" + elementRow).attr('class', 'row-delete-higlight');

                }
            }
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
                            console.log(data.sample_data);
                            $("#sample_description_name").html(data.sample_data.sampleName);
                        },
                        error: function () {
                            alert("Couldn't resolve Sample details!");
                        }
                    });

                }
            }
        }

        function do_sample_delete_confirmation(event) {
            var targetId = $($(event.target)).attr("id");

            $("#delete_component").html(" Sample ");
            $("#delete_component_message").html(" sample");

            var literalPart = "sample_delete";
            var rowLiteralPart = "_sample_row";

            if (typeof targetId !== "undefined") {
                if (targetId.slice(-(parseInt(literalPart.length))) == literalPart) {
                    elementId = targetId.slice(0, -(parseInt(literalPart.length + 1)));
                    elementRow = elementId + rowLiteralPart;

                    $("#target_delete_id").val(elementId + "_sample");
                    $("#" + elementRow).attr('class', 'row-delete-higlight');
                }
            }
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
                    'task': 'assign_samples_to_studies',
                    'ena_collection_id': ena_collection_id,
                    'study_id': studyId,
                    'selected_study_samples': selected_study_samples,
                    'excluded_study_samples': excluded_study_samples
                },
                success: function (data) {
                    refresh_table_data(data, "samples");

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

            //get all existing samples, and...
            //remove the highlight from all them
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
            }

            do_disengage_studyComponentsDeleteModal();
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
            var elementRow = targetId + "_row";

            $("#" + elementRow).removeClass("row-delete-higlight");
            $("#target_delete_id").val("");
            $('#studyComponentsDeleteModal').modal('hide');

            refresh_tool_tips();
        }

        function refresh_tool_tips() {
            $("[data-toggle='tooltip']").tooltip();
            $('[data-toggle="popover"]').popover();
        }

        function dispatch_delete_task() {
            var targetId = $("#target_delete_id").val();
            var targetComponent = targetId.split("_")[1];
            var elementId = targetId.split("_")[0];

            if (targetComponent == "sample") {
                do_delete_sample(elementId);
            } else if (targetComponent == "publication") {
                do_delete_publication(elementId);
            } else if (targetComponent == "contact") {
                do_delete_contact(elementId);
            }

        }


    }
)
