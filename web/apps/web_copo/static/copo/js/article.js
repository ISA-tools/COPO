/**
 * felix.shaw@tgac.ac.uk - 01/05/15.
 */


$(document).ready(function(){
    'use strict';
    $('#btn_submit_to_figshare').on('click', submit_to_figshare)
    $('#btn_save_article').on('click', save_article)

    $('#input_text').on("keypress", function(e) {
	        if (e.keyCode == 13) {
	            e.preventDefault()
	        	var input = $(this).val()
				var tags = input.split(',')
				for(var i = 0; i < tags.length; i++){
					$(this).val('')
					var text = '<span class="label label-info">' + tags[i] + '<span class="glyphicon glyphicon-remove delete_tag" aria-hidden="true"></span></span>'
					$('#tags_input').append(text)

					$('.delete_tag').on('click', function(e){
						$(this).parent().remove()
					})
				}
			}
	});

    // Change this to the location of your server-side upload handler:
    $('#fileupload').fileupload({
        url: '/rest/small_file_upload/',
        dataType: 'json',
        done: function (e, data) {
            var text = ''
            $.each(data.result, function (index, file) {
                text = text + '<span class="label label-success"><span class="glyphicon glyphicon-picture" aria-hidden="true"></span><span class="spacer"></span>' + file.name + '</span><span class="spacer"></span><input type="hidden" value="' + file.id + '"/>'
            });

            $('#files').append(text)
            $('#progress').hide()
            $('#upload_files_button').hide()
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

function save_article(e){
    'use strict'
    e.preventDefault()
    var file_ids = $('#files').children('input')
    var files = []
    $.each(file_ids, function(index, value){
        files.push($(value).val())
    })
    var raw_tags = $('#tags_input').children('.label')
    var tags = []
    $.each(raw_tags, function(index, value){
        tags.push($(value).text())
    })
    var token = $.cookie('csrftoken')
    $.ajax({
        headers: {'X-CSRFToken':token},
        type:"POST",
        url:"/copo/save_article/",
        dataType:"json",
        data:{"files": files, "tags": tags}
    }).done(function(data){
        console.log(data)
    })

}


