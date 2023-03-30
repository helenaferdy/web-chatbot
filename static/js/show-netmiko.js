$(document).ready(function() {
    $('#submit').click(function(event) {
        const aElement = document.getElementById('device-select');
        const device = aElement.textContent.trim();
        console.log(device);

        event.preventDefault();
        var input = $('#input').val();
        var inputHTML = '<div class="user"><li id="user">' + input + '</li></div>';
        $("#output").append(inputHTML);
        $('#input').val('');
        $('#loading').text('Loading . . . .'); 

        $.ajax({
            type: 'POST',
            url: '/get_show_netmiko',
            contentType: 'application/json',
            data: JSON.stringify({input, device}),
            success: function(response) {

                var html = '';
                html += '<div class="assistant">';
                $.each(response, function(index, item) {
                    $.each(item, function(key, value) {
                        html += '<li id="assistant">' + key + ': ' + value + '</li>';
                      });
                    html += '<br>'
                });
                html += '</div>';
                $("#output").append(html);
                $('#loading').text(' \200 '); 
            },
            error: function(error) {
                console.log(error);
            }
        });
      });


      
});


