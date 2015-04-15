$(document).ready(function () {
    $('#frm_initiate_button').on('click', function () {
        before_repo_upload(); //do some housekeeping

        var handle = 0
        //var postData = $("#frm_initiate_repo").serializeArray();
        var formURL = $("#frm_initiate_repo").attr("action");
        var csrftoken = $.cookie('csrftoken');

        $.ajax(
            {
                url: formURL,
                type: "POST",
                headers: {'X-CSRFToken': csrftoken},
                //data: postData,
                success: function (data) {
                    clearInterval(handle);
                    handle = 0;
                    after_repo_upload(data);
                },
                error: function () {
                    alert('no data returned')
                }
            });
        handle = setInterval(get_feedback, 1000);
    });

    function get_feedback() {
        $.ajax({
            type: "GET",
            url: "/copo/repo_feedback/",
            dataType: "json",
            success: function (data) {
                during_repo_upload(data);
            },
            error: function () {
                alert('no data returned')
            }
        });
    }

    function before_repo_upload() {
        $("#repo-feedback-1").attr("style", "width: 0%");
        $("#repo-feedback-span-1").html("0% Complete");
        $("#frm_initiate_button").prop("disabled", true);
        $("#repo-feedback-cnt-1").hide();
    }

    function after_repo_upload(data) {
        var j = data.exit_status;
        $( "#repo-alert-span-1" ).html( "<strong>Success!</strong> File humming in repo" );
        //$( "#repo-alert-span-1" ).html( j );
        $("#repo-feedback-cnt-1").hide();
        $("#repo-alert-cnt-1").show();
    }

    function during_repo_upload(data) {
        if(parseInt(data.pct_complete)>0) {
            $("#repo-feedback-cnt-1").show();
        }
        $( "#repo-feedback-1" ).attr( "style", "width: "+data.pct_complete+"%");
        $( "#repo-feedback-span-1" ).html( data.pct_complete+"%" );
    }

}) //end of document.ready