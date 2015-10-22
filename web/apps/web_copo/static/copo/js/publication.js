$(document).ready(function () {

        //do some housekeeping, encapsulates all dangling event definitions
        do_housekeeping();

        function do_housekeeping() {

            //handles event to show/hide study reference/type form
            $('#btn_add_new_publication').on('click', function () {
                do_add_publication();
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

            formURL = $("#add_new_publication_form").attr("action");
            csrftoken = $.cookie('csrftoken');

            $.ajax({
                url: formURL,
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    'task': 'save',
                    'auto_fields': auto_fields
                },
                success: function (data) {
                    //refresh_table_data(data, "publications");
                    alert("ping!")
                },
                error: function () {
                    alert("Couldn't retrieve publications!");
                }
            });
        }


    }
)
