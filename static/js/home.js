"strict";
// Foco nos cnpjs após mudança de página e nova requisição
window.onload = function () {
  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("pagina")) {
    document.getElementById("section-2").scrollIntoView();
  }
};

// Popup - Popup
const modal = document.querySelector(".popup");

// Popup - Setas
const closeModal = document.querySelector("#close-arrow");
const paymentToPricing = document.querySelector("#payment-pricing-arrow");
const endToPayment = document.querySelector("#to-payment-arrow");

// Popup - Seções
const pricingSection = document.querySelector(".popup__section--pricing");
const paymentSection = document.querySelector(".popup__section--payment");
const endSection = document.querySelector(".popup__section--end");

// Popup - Botões
const openModal = document.querySelector(".baixar-btn");
const baixarBtn = document.querySelector(".pricing__second-btn");
const toEndBtn = document.querySelector(".payment__btn");
const endBtn = document.querySelector(".end__btn");

// Popup - Abrir e fechar
openModal.addEventListener("click", function () {
  modal.showModal();
});

closeModal.addEventListener("click", function () {
  modal.close();
});

// Popup - Mudador de seção
const changeSection = function (from, to) {
  from.style.display = "none";
  to.style.display = "block";
};

const createChangeSectionEvent = function (element, from, to) {
  element.addEventListener("click", function () {
    changeSection(from, to);
  });
};

// Popup - Pricing -> Payment
createChangeSectionEvent(baixarBtn, pricingSection, paymentSection);

// Popup - Payment -> Pricing
createChangeSectionEvent(paymentToPricing, paymentSection, pricingSection);

// Popup - Payment -> End
createChangeSectionEvent(toEndBtn, paymentSection, endSection);

// Popup - Encerramento
endBtn.addEventListener("click", function () {
  modal.close();
  changeSection(endSection, pricingSection);
});
