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
                var outputHTML = '<div class="assistant"><li id="assistant">' + device + ' : ' + input + '</li></div>';
                $("#output").append(outputHTML);

                var html = '';
                html += '<div class="row">';
                $.each(response, function(index, item) {
                    html += '<div class="col-lg-3">';
                    html += '<div class="card border-dark mb-3" style="max-width: 20rem;">';
                    $.each(item, function(key, value) {
                        // html += '<li id="assistant">' + key + ': ' + value + '</li>';
                        html += '<div class="card-header">' + key + '</div>';
                        html += '<div class="card-body">';
                        html += '<p class="card-text">' + value + '</p>';
                        html += '</div>';
                      });
                    html += '</div>';
                    html += '</div>';
                });
                html += '</div>';
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


