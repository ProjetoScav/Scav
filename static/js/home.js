"strict";

// const flaskToken = document.querySelector("#token").value;

document.addEventListener("scroll-to-results", () => {
  document.querySelector(".app").scrollIntoView({ behavior: "smooth" });
});

document.addEventListener("alpine:init", function () {
  Alpine.data("dropdown", () => ({
    open: false,
    toggle() {
      this.open = !this.open;
    },
  }));
});

// Função de remoção de popups
remove_popups = function () {
  try {
    download_popup = document.querySelector(".popup__section");
    download_popup.remove();
  } catch (error) {}
  try {
    login_popup = document.querySelector(".login-popup");
    login_popup.remove();
  }   catch (error) {}
};

// Exclusão dos popups com esc
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    remove_popups();
  }
});

// Exclusão dos popups com click no backdrop
backdrop = document.querySelector(".backdrop");
backdrop.addEventListener("click", function () {
  remove_popups();
});
