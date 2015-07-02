/**
 * Created by fshaw on 16/02/15.
 */

$(document).ready(function () {


    $('.spinner').hide()
    $('.coolHandLuke li').on('click', function (e) {
        if ($(e.target).prev().hasClass('red')) {
            submit_to_figshare(e)
        }
        else {
            view_in_figshare(e)
        }

    })

    //hide delete button for first element in the study type group
    $("#study_types_lists_div").find('.study_type_select_divs:first').children(":nth-child(2)").hide();

    //handle change event for collection types drop-down
    toggle_collection_type($("#collection_type option:selected").val());

    $("#collection_type").change(function () {
        toggle_collection_type($("#collection_type option:selected").val());
    });

    //handle event for add study type
    $("#study_type_add").click(function (event) {
        do_add_study_type();
    });

    //handle click event for delete study type
    $("#study_types_lists_div").on('click', 'a.study_type_remove', function (event) {
        do_remove_study_type(event);
    });


    function do_add_study_type() {
        var clonableTarget = $("#study_types_lists_div").find('.study_type_select_divs:last').clone();

        // update the id, name of the clone
        var fc = clonableTarget.children(":first").children(":first");
        var num_app = fc.attr("id").split("_");
        fc.attr("id", num_app[0] + "_" + (parseInt(num_app[1]) + 1));
        fc.attr("name", num_app[0] + "_" + (parseInt(num_app[1]) + 1));

        clonableTarget.children(":nth-child(2)").show();
        clonableTarget.children(":nth-child(2)").css("display","inline-block");
        $("#study_types_lists_div").append(clonableTarget);
    }

    function do_remove_study_type(event) {
        var par = $($(event.target)).parents(":eq(2)")
        par.remove();
    }

    function toggle_collection_type(collection_type) {
        if (collection_type.toLocaleLowerCase() == "ena submission") {
            $("#study_type_div").show();
        } else {
            $("#study_type_div").hide();
        }
    }


    function submit_to_figshare(e) {
        e.preventDefault()

        var spinner = $(e.target).closest('td').find('.spinner')
        var color_span = $(e.target).prev()
        $(spinner).show()

        // ajax call checks if figshare creds are valid
        $.ajax({
            type: "GET",
            url: "/rest/check_figshare_credentials",
            dataType: "json"
        }).done(function (data) {
            // if creds invalid, prompt user
            if (data.exists == false) {
                url = data.url
                window.open(url, "_blank", "toolbar=no, scrollbars=yes, resizable=no, top=500, left=20, width=800, height=600");
            }
            // if creds valid call submit_to_figshare backend handler
            else {
                var article_id = $(e.target).closest('tr').attr('data-collection_id')
                $.ajax({
                    type: "GET",
                    url: "/api/submit_to_figshare/" + article_id,
                    dataType: "json"
                }).done(function (data, textStatus, xhr) {

                    if (data.success == true) {

                        BootstrapDialog.show({
                            title: 'Success',
                            message: 'Figshare Object Deposited'
                        });
                        $(color_span).removeClass('red').addClass('green')
                        $(e.target).text('Inspect')
                    }
                    $(spinner).hide()
                })
            }
        })
    }


})
