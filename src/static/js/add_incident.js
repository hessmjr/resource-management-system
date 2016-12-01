
function validateForm(submit_val) {

    // skip validation if user canceled
    if (submit_val == "Cancel")
        return true;

    // scroll to top after submitting
    $('html, body').animate({ scrollTop: 0 }, 0);

    // remove all errors if any exist
    $('div').remove('.error');

    // get all form values
    var desc_sel = $('#description');
    var date_sel = $('#date');
    var lat_sel = $('#lat');
    var long_sel = $('#long');

    // header selector for adding errors
    var header_sel = $('.header');

    // regex patterns
    var descPattern = /^[\w \-\.]+/;
    var latPattern = /^-?([1-8]?[1-9]|[1-9]0)\.\d{1,6}$/;
    var longPattern = /^-?(1[1-8][1-9]|[0-9]{1,2})\.\d{1,6}$/;
    var datePattern = /^\d{2}\/\d{2}\/\d{4}$/;

    // validate date
    if (date_sel.val() == "") {
        header_sel.after(buildError('Please enter a date'));
        return false;
    } else if (!datePattern.test(date_sel.val())) {
        header_sel.after(buildError('Please enter date like MM/DD/YYYY'));
        return false;
    }

    // validate description
    if (desc_sel.val() == "") {
        header_sel.after(buildError('Please enter a description'));
        return false;
    } else if (!descPattern.test(desc_sel.val())) {
        header_sel.after(buildError('Please enter a valid description'));
        return false;
    }

    // validate the latitude
    if (lat_sel.val() == "") {
        header_sel.after(buildError('Please enter a latitude'));
        return false;
    } else if (!latPattern.test(lat_sel.val())) {
        header_sel.after(buildError('Please enter a valid latitude'));
        return false;
    }

    // validate the longitude
    if (long_sel.val() == "") {
        header_sel.after(buildError('Please enter a longitude'));
        return false;
    } else if (!longPattern.test(long_sel.val())) {
        header_sel.after(buildError('Please enter a valid longitude'));
        return false;
    }


    // all is good to submit
    return true;
}


function buildError(message) {
    return '<div class="row"><div class="col s12 red-text error center"><h6>' +
        '<h6><strong>Error:</strong> ' + message + ' </h6></div></div>'
}
