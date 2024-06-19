document.addEventListener("DOMContentLoaded", function () {
  const galleryList = document.getElementById("gallery-list");

  function fetchGallery(sortBy = "new") {
    fetch(`/gallery?sort=${sortBy}`)
      .then((response) => response.json())
      .then((data) => {
        galleryList.innerHTML = "";
        data.forEach((item) => {
          const listItem = document.createElement("li");
          listItem.setAttribute("data-id", item.id);
          listItem.innerHTML = `
              <img src="${item.image}" alt="${item.name}">
              <div class="overlay">
                <span class="text">${item.name}</span>
                <button class="heart">❤️</button>
              </div>
            `;
          listItem.addEventListener("click", function () {
            window.location.href = `gallery-item.html?id=${item.id}`;
          });
          galleryList.appendChild(listItem);
        });
      })
      .catch((error) => console.error("Ошибка:", error));
  }

  document.getElementById("popular").addEventListener("click", function () {
    fetchGallery("popular");
  });

  document.getElementById("new").addEventListener("click", function () {
    fetchGallery("new");
  });

  // Fetch gallery items initially sorted by new
  fetchGallery();
});
