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
