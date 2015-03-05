$(document).ready(function(){

    $("#frm_login_submit").on('click', function() {
        //frm_login_submit_callback($(this));
    });



});

function frm_login_submit_callback(request){

    //add ajax query to get orchid stuff
    //get username and pasword
    var username = $("#frm_login_username").val();
    var password = $("#frm_login_password").val();

    if((username)&&(password)){

        $.ajax({
            type: "POST",
            url:"?xhr",
            data: {
                'username': username,
                'password': password
            },
            success: function(data){

                //results = $(data).find('#results').html()
                alert(data);

            },
            error: function(){
                alert("Error");
            }
        })
    }


}