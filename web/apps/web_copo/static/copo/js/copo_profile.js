/**
 * felix.shaw@tgac.ac.uk - 22/10/15.
 */
$(document).ready(function () {
    $('.publication').click(function () {
        var url = $('#publications_url').val()
        console.log(url)
        window.location.href = url
    })
})
