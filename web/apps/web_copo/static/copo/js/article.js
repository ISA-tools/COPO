/**
 * felix.shaw@tgac.ac.uk - 01/05/15.
 */


$(document).ready(function(){
    $('#btn_submit_to_figshare').on('click', submit_to_figshare)
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
