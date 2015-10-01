var formURL = "";
var transfer_id = "";
var handle = 0;
var csrftoken = "";

$(document).ready(function () {
    //handle repo upload: sends selected file to the repo via aspera
    $("body").on('click', 'a.repo-upload', function (event) {
        event.preventDefault();
        do_repo_upload(event);
    });


    function do_repo_upload(event) {
        before_repo_upload(); //do some housekeeping

        var data_file_id = $($(event.target)).parent().attr("target-id");

        var ena_collection_id = $("#ena_collection_id").val();
        var study_id = $("#study_id").val();

        var csrftoken = $.cookie('csrftoken');

        $.ajax(
            {
                url: "/copo/upload_to_dropbox/",
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    'task': 'initiate_transfer',
                    'ena_collection_id': ena_collection_id,
                    'study_id': study_id,
                    'data_file_id': data_file_id
                },
                success: function (data) {
                    console.log(data);
                    //if (data.initiate_status == "error") {
                    //    imessage = 'No data returned!'
                    //    report_error(imessage);
                    //    terminate_process();
                    //} else if (data.initiate_status == "success") {
                    //    transfer_id = data.transfer_id;
                    //    start_process();
                    //}
                },
                error: function () {
                    //imessage = 'No data returned!'
                    //report_error(imessage);
                    //terminate_process();
                }
            });
    }

    function aspera_report() {
        $.ajax({
            type: "GET",
            url: formURL,
            dataType: "json",
            data: {'transfer_id': transfer_id},
            success: function (data) {
                report_transfer_progress(data);
            },
            error: function () {
                alert('no data returned')
            }
        });
    }

    function start_process() {
        handle = setInterval(aspera_report, 1000);
    }

    function terminate_process() {
        clearInterval(handle);
        handle = 0;
    }

    function before_repo_upload() {
        $("#repo-feedback-1").attr("style", "width: 0%");
        $("#repo-feedback-span-1").html("0% Complete");
        $("#frm_initiate_button").prop("disabled", true);
        $("#repo-feedback-cnt-1").hide();
    }

    function report_error(imessage) {
        $("#repo-alert-cnt-1").attr('class', 'alert alert-danger alert-dismissible');
        $("#repo-alert-span-1").html("<strong>Error:</strong> " + imessage);
        $("#repo-feedback-cnt-1").hide();
        $("#repo-alert-cnt-1").show();
    }

    function report_post_transfer_success() {
        $("#repo-alert-span-1").html("<strong>Success:</strong> File humming in repo!");
        $("#repo-feedback-cnt-1").hide();
        $("#repo-alert-cnt-1").show();
    }

    function report_transfer_progress(data) {
        if (data.exit_status == "") {
            if (parseInt(data.pct_complete) > 0) {
                $("#repo-feedback-cnt-1").show();
            }
            $("#repo-feedback-1").attr("style", "width: " + data.pct_complete + "%");
            $("#repo-feedback-span-1").html(data.pct_complete + "%");
        } else if (data.exit_status == "success") {
            report_post_transfer_success();
            terminate_process();
        } else {
            imessage = "Error!";
            report_error(imessage);
            terminate_process();
        }
    }

}) //end of document.ready