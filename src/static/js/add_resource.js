
$(document).ready(function() {
    $('select').material_select();
});


$( function () {

    $("#add-capability").on("click", addCapability);

    function addCapability(e) {
        e.preventDefault();
        var $newCapability = $("#new-capability");

        var newCapabilityVal = $newCapability.val();
        if (newCapabilityVal != "") {
            var selectList = $("#capabilities");
            var newOption = "<option selected='selected' value='" +
                newCapabilityVal + "'>" + newCapabilityVal + "</option>";
            selectList.append(newOption);
            $newCapability.val("");
        }
    }

});

function validateForm(submit_val) {

    // skip validation if user canceled
    if (submit_val == "Cancel")
        return true;

    // scroll to top after submitting
    $('html, body').animate({ scrollTop: 0 }, 0);

    // remove all errors if any exist
    $('div').remove('.error');

    // get all form values
    var name_sel = $('#name');
    var model_sel = $('#model');
    var lat_sel = $('#lat');
    var long_sel = $('#long');
    var amount_sel = $('#amount');

    // header selector for adding errors
    var header_sel = $('.header');

    // regex patterns
    var namePattern = /[\w \-\.]+/;
    var latPattern = /^-?([1-8]?[1-9]|[1-9]0)\.\d{1,6}$/;
    var longPattern = /^-?(1[1-8][1-9]|[0-9]{1,2})\.\d{1,6}$/;
    var amountPattern = /[\d]+(\.[\d]{2})?/;

    // validate name
    if (name_sel.val() == "") {
        header_sel.after(buildError('Please enter a name'));
        return false;
    } else if (!namePattern.test(name_sel.val())) {
        header_sel.after(buildError('Please enter a valid name'));
        return false;
    }

    // validate model
    if (model_sel.val() == "") {
        header_sel.after(buildError('Please enter a model'));
        return false;
    } else if (!namePattern.test(model_sel.val())) {
        header_sel.after(buildError('Please enter a valid model'));
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

    // validate the amount
    if (amount_sel.val() == "") {
        header_sel.after(buildError('Please enter a amount'));
        return false;
    } else if (!amountPattern.test(amount_sel.val())) {
        header_sel.after(buildError('Please enter a amount'));
        return false;
    } else if (parseFloat(amount_sel.val()) < 0) {
        header_sel.after(buildError('Amount must be positive'))
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
