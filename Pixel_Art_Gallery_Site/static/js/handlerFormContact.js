document.getElementById('feedbackForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы по умолчанию

    // Собираем данные из формы
    const formData = new FormData(this);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        comment: formData.get('comment')
    };

    // Отправляем данные на бэкенд
    fetch('/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.text())
    .then(responseText => {
        alert(responseText); // Отображаем ответ от сервера
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});