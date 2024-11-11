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

// Exclusão do popup com click no backdrop
// Todo: inclusão da funcionalidade no login popup
backdrop = document.querySelector(".backdrop");
backdrop.addEventListener("click", function () {
  download_popup = document.querySelector(".popup__section");
  // login_popup = document.querySelector("");
  download_popup.remove()
});