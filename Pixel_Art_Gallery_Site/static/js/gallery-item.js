document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);
  const itemId = params.get("id");

  if (itemId) {
    fetch(`/gallery_item/${itemId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert(data.message);
        } else {
          document.getElementById("item-name").textContent = data.name;
          document.getElementById("item-image").src = `${data.image}`;
          document.getElementById("item-image").alt = data.name;
          document.getElementById(
            "item-author"
          ).textContent = `Автор: ${data.author}`;
          document.getElementById(
            "item-tools"
          ).textContent = `Используемые программы: ${data.tools}`;

          const commentsList = document.getElementById("comments-list");
          data.comments.forEach((comment) => {
            const commentItem = document.createElement("li");
            commentItem.innerHTML = `
                            <img src="./images/user-avatar.png" alt="user avatar" />
                            <div class="user">
                                <div class="user-name-date">
                                    <p class="user-name-date__name">${comment.name}</p>
                                    <p class="user-name-date__date">${comment.date}</p>
                                </div>
                                <p class="user__comment">${comment.comment}</p>
                            </div>
                        `;
            commentsList.appendChild(commentItem);
          });
        }
      })
      .catch((error) => console.error("Ошибка:", error));

    document
      .getElementById("comment-form")
      .addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("comment-name").value;
        const comment = document.getElementById("comment-text").value;

        fetch("/submit_comment", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            gallery_item_id: itemId,
            name: name,
            comment: comment,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            alert(data.message);
            location.reload();
          })
          .catch((error) => console.error("Ошибка:", error));
      });
  } else {
    alert("ID элемента не указан");
  }
});
