$(function() {
            $('#btnAgregar').click(function() {
                $.ajax({
                    url: '/agregar',
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