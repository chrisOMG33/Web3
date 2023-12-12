$(function() {
            $('#btnModificar').click(function() {
                $.ajax({
                    url: '/exec_modificar',
                    data: $('form').serialize(),
                    type: 'POST',
                    success: function(response) {
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });
        });
