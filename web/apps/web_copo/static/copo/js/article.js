/**
 * felix.shaw@tgac.ac.uk - 01/05/15.
 */


$(document).ready(function(){
    $('#btn_submit_to_figshare').on('click', submit_to_figshare)



    'use strict';
    // Change this to the location of your server-side upload handler:
    $('#fileupload').fileupload({
        url: '/rest/small_file_upload/',
        dataType: 'json',
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo('#files');
            });
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        },
        add: function(e, data) {
            data.submit();
        }

    })
})

function submit_to_figshare(e){
    e.preventDefault()
    $.ajax({
        type:"GET",
        url:"/rest/check_figshare_credentials",
        dataType:"json"
    }).done(function(data){
        if(data.exists == false) {
            url = data.url
            window.open(url, "_blank", "toolbar=no, scrollbars=yes, resizable=no, top=500, left=20, width=800, height=600");
        }
    })
}


