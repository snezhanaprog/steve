document
  .getElementById("galleryForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Предотвращаем отправку формы по умолчанию

    // Собираем данные из формы
    const formData = new FormData(this);

    // Отправляем данные на бэкенд
    fetch("/submit_gallery_item", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((responseData) => {
        alert(responseData.message); // Отображаем ответ от сервера
      })
      .catch((error) => {
        console.error("Ошибка:", error);
      });
  });
