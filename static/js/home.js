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

// Exclusão dos popups com esc
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    remove_popups();
  }
});

// Exclusão dos popups com click no backdrop
// Todo: inclusão da funcionalidade no login popup
backdrop = document.querySelector(".backdrop");
backdrop.addEventListener("click", function () {
  remove_popups();
});

remove_popups = function () {
  download_popup = document.querySelector(".popup__section");
  login_popup = document.querySelector(".login-popup");
  download_popup.remove();
  login_popup.remove();
};
