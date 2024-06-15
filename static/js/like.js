$(document).ready(function () {
    var isRequestPending = false;
    $('.like-form').on('submit', function (event) {
        event.preventDefault();
        if (isRequestPending) return;

        var $form = $(this);
        isRequestPending = true;
        console.log($form);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function (response) {
                var $qaDiv = $form.closest('.qa-item');
                $qaDiv.find('.like-score').text(response.rating);
                isRequestPending = false;
            },
            error: function (response) {
                alert('Error: ' + response.responseJSON.error);
                isRequestPending = false;
            }
        });
    });
});