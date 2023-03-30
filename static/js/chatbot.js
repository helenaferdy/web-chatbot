$(document).ready(function() {
    $('#submit').click(function() {
        var input = $('#input').val();
        var inputHTML = '<div class="user"><li id="user">' + input + '</li></div>';
        $("#output").append(inputHTML);
        $('#input').val('');
        $('#loading').text('Loading . . . .'); 

        $.ajax({
            type: 'POST',
            url: '/get_chatbot',
            contentType: 'application/json',
            data: JSON.stringify({input}),
            success: function(response) {
                var result = response.result
                var inputHTML = '<div class="assistant"><li id="assistant">' + result + '</li></div>';
                $("#output").append(inputHTML);
                $('#loading').text(' \200 '); 
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

