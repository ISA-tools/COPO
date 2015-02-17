/**
 * Created by fshaw on 16/02/15.
 */

$(document).ready(function(){

    $('#submit_to_repo_btn').on('click', submit_to_repo)

    function submit_to_repo(event){
        //get list of collections to submit
        var collections = $('#browse_table tr:not(:first)')
        //get csrf token value from cookie
        var token = $.cookie('csrftoken');
        $(collections).each(function(key, value){
            collection_id = $(value).children('td:first').attr('data-collection_id')
            $.ajax({
              headers: {'X-CSRFToken':token},
              type: "POST",
              url: '/rest/submit_collection/',
              data: {'collection_id':collection_id},
              success: function(data){
                  console.log(data)
              },
              dataType: 'json'
            });
        })
    }
})