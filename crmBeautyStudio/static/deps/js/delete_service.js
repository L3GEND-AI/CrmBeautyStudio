$(document).ready(function() {
    $('.delete-service-btn').click(function() {
        var serviceId = $(this).data('service-id');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        if (confirm("Вы уверены, что хотите удалить эту услугу?")) {
            $.ajax({
                url: '/services/delete/' + serviceId + '/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    // Remove the row from the table
                    $('#service-row-' + serviceId).remove();
                    alert('Услуга успешно удалена');
                },
                error: function(xhr, status, error) {
                    alert('Ошибка удаления услуги');
                }
            });
        }
    });
});
