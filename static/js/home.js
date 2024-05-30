"strict";

const flaskToken = document.querySelector("#token").value;

document.addEventListener("scroll-to-results", () => {
  document.querySelector(".results").scrollIntoView({ behavior: "smooth" });
});

// Popup - Seções
const pricingSection = document.querySelector(".popup__section--pricing");
const paymentSection = document.querySelector(".popup__section--payment");
const endSection = document.querySelector(".popup__section--end");

// Popup - Botões
const openModal = document.querySelector(".baixar-btn");
const baixarBtn = document.querySelector(".pricing__first-btn");
const toEndBtn = document.querySelector(".payment__btn");
const endBtn = document.querySelector(".end__btn");

// const changePaymentEnd = function (element, from, to) {
//   element.addEventListener("click", function () {
//     if (isEmail) {
//       from.style.display = "none";
//       to.style.display = "block";
//       document.querySelector(".payment__email").classList.remove("outline-red");
//       document
//         .querySelector(".payment__email-subtext")
//         .classList.remove("color-red");
//       document.querySelector(".payment__email-subtext").textContent =
//         "*O arquivo será enviado para o email inserido";
//       // sendEmailData(inputEmail.value);
//     } else {
//       document.querySelector(".payment__email").classList.add("outline-red");
//       document.querySelector(".payment__email").focus();
//       document
//         .querySelector(".payment__email-subtext")
//         .classList.add("color-red");
//       document.querySelector(".payment__email-subtext").textContent =
//         "* Insira um email válido";
//     }
//   });
// };

// Popup - Payment -> End
// changePaymentEnd(toEndBtn, paymentSection, endSection);
