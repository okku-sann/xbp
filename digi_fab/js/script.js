(() => {
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modal-img");
  const caption = document.getElementById("caption");
  const closeButton = document.querySelector(".close");

  if (!modal || !modalImg) {
    return;
  }

  document.querySelectorAll(".photo-item img").forEach((image) => {
    image.addEventListener("click", () => {
      modal.style.display = "flex";
      modalImg.src = image.src;
      modalImg.alt = image.alt || "";
      if (caption) {
        caption.textContent = image.alt || "";
      }
    });
  });

  const closeModal = () => {
    modal.style.display = "none";
    modalImg.removeAttribute("src");
  };

  closeButton?.addEventListener("click", closeModal);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.style.display === "flex") {
      closeModal();
    }
  });
})();
