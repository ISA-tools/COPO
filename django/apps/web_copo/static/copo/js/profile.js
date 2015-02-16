/**
 * Created by fshaw on 16/02/15.
 */

$(document).ready(function(){

    $('#submit_to_repo_btn').on('click', submit_to_repo)

    function submit_to_repo(event){
        //get list of collections to submit
        var collections = $('#browse_table tr')
        console.log(collections)
    }

})