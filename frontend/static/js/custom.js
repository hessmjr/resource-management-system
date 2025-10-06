
$(document).ready(function() {
    // Initialize Materialize components
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});


$.fn.exists = function () {
    return this.length !== 0;
}


// Capability handler is now implemented inline in templates for better modularity

function validateForm(submit_val) {

    // skip validation if user canceled
    if (submit_val == "Cancel")
        return true;

    // scroll to top after submitting
    $('html, body').animate({ scrollTop: 0 }, 0);

    // remove all errors if any exist
    $('div').remove('.error');

    // get any form values
    var name_sel = $('#name');
    var model_sel = $('#model');
    var lat_sel = $('#lat');
    var long_sel = $('#long');
    var amount_sel = $('#amount');
    var desc_sel = $('#description');
    var date_sel = $('#date');

    // header selector for adding errors
    var header_sel = $('.header');

    // regex patterns
    var namePattern = /[\w \-\.]+/;
    var latPattern = /^-?([1-8]?[0-9]|[1-9]0)\.\d{1,6}$/;
    var longPattern = /^-?(1[0-8][0-9]|[0-9]{1,2})\.\d{1,6}$/;
    var amountPattern = /[\d]+(\.[\d]{2})?/;
    var descPattern = /^[\w \-\.]+/;
    var datePattern = /^\d{4}-\d{2}-\d{2}$/;

    // validate name
    if (name_sel.exists() && name_sel.val() == "") {
        header_sel.after(buildError('Please enter a name'));
        return false;
    } else if (name_sel.exists() && !namePattern.test(name_sel.val())) {
        header_sel.after(buildError('Please enter a valid name'));
        return false;
    }

    // validate model
    if (model_sel.exists() && model_sel.val() == "") {
        header_sel.after(buildError('Please enter a model'));
        return false;
    } else if (model_sel.exists() && !namePattern.test(model_sel.val())) {
        header_sel.after(buildError('Please enter a valid model'));
        return false;
    }

    // validate the latitude
    if (lat_sel.exists() && lat_sel.val() == "") {
        header_sel.after(buildError('Please enter a latitude'));
        return false;
    } else if (lat_sel.exists() && !latPattern.test(lat_sel.val())) {
        header_sel.after(buildError('Please enter a valid latitude'));
        return false;
    }

    // validate the longitude
    if (long_sel.exists() && long_sel.val() == "") {
        header_sel.after(buildError('Please enter a longitude'));
        return false;
    } else if (long_sel.exists() && !longPattern.test(long_sel.val())) {
        header_sel.after(buildError('Please enter a valid longitude'));
        return false;
    }

    // validate the amount
    if (amount_sel.exists() && amount_sel.val() == "") {
        header_sel.after(buildError('Please enter an amount'));
        return false;
    } else if (amount_sel.exists() && !amountPattern.test(amount_sel.val())) {
        header_sel.after(buildError('Please enter an amount'));
        return false;
    } else if (amount_sel.exists() && parseFloat(amount_sel.val()) < 0) {
        header_sel.after(buildError('Amount must be positive'))
        return false;
    }

    // validate date
    if (date_sel.exists() && date_sel.val() == "") {
        header_sel.after(buildError('Please enter a date'));
        return false;
    } else if (date_sel.exists() && !datePattern.test(date_sel.val())) {
        header_sel.after(buildError('Please enter date like YYYY-MM-DD'));
        return false;
    }

    // validate description
    if (desc_sel.exists() && desc_sel.val() == "") {
        header_sel.after(buildError('Please enter a description'));
        return false;
    } else if (desc_sel.exists() && !descPattern.test(desc_sel.val())) {
        header_sel.after(buildError('Please enter a valid description'));
        return false;
    }

    // all is good to submit
    return true;
}


function buildError(message) {
    console.log("here");
    return '<div class="row"><div class="col s12 red-text error center"><h6>' +
        '<h6><strong>Error:</strong> ' + message + ' </h6></div></div>'
}
