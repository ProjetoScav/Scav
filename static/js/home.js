"strict";

const flaskToken = document.querySelector("#token").value;

document.addEventListener("scroll-to-results", () => {
  document.querySelector(".results").scrollIntoView({ behavior: "smooth" });
});

document.addEventListener("alpine:init", function () {
  Alpine.data("dropdown", () => ({
    open: false,
    toggle() {
      this.open = !this.open;
    },
  }));
});
console.log(Alpine);
