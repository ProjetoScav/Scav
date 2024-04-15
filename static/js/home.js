"strict";
// Foco nos cnpjs após mudança de página e nova requisição
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("pagina")) {
    document.getElementById("section-2").scrollIntoView();
  }
};

// Popup - Popup
const modal = document.querySelector(".popup");

// Popup - Setas
const closeModal = document.getElementsByClassName("close");
const paymentToPricing = document.querySelector("#payment-pricing-arrow");
const endToPayment = document.querySelector("#to-payment-arrow");

// Popup - Seções
const pricingSection = document.querySelector(".popup__section--pricing");
const paymentSection = document.querySelector(".popup__section--payment");
const endSection = document.querySelector(".popup__section--end");

// Popup - Botões
const openModal = document.querySelector(".baixar-btn");
const baixarBtn = document.querySelector(".pricing__first-btn");
const toEndBtn = document.querySelector(".payment__btn");
const endBtn = document.querySelector(".end__btn");

// Popup - Abrir e fechar
openModal.addEventListener("click", function () {
  modal.showModal();
});

for (let i = 0; i < closeModal.length; i++) {
  closeModal[i].addEventListener("click", function () {
    modal.close();
  });
}

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

// Popup - Envio de email
const sendEmailData = function (email) {
  fetch("download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("#token").value,
    },
    body: JSON.stringify({ "pay-email": email }),
  }).then((response) => console.log(response));
};

const changePaymentEnd = function (element, from, to) {
  element.addEventListener("click", function () {
    if (isEmail) {
      from.style.display = "none";
      to.style.display = "block";
      document.querySelector(".payment__email").classList.remove("outline-red");
      document
        .querySelector(".payment__email-subtext")
        .classList.remove("color-red");
      document.querySelector(".payment__email-subtext").textContent =
        "*O arquivo será enviado para o email inserido";
      sendEmailData(inputEmail.value);
    } else {
      document.querySelector(".payment__email").classList.add("outline-red");
      document.querySelector(".payment__email").focus();
      document
        .querySelector(".payment__email-subtext")
        .classList.add("color-red");
      document.querySelector(".payment__email-subtext").textContent =
        "* Insira um email válido";
    }
  });
};

// Popup - Pricing -> Payment
createChangeSectionEvent(baixarBtn, pricingSection, paymentSection);

// Popup - Payment -> Pricing
createChangeSectionEvent(paymentToPricing, paymentSection, pricingSection);

// Popup - Payment -> End
changePaymentEnd(toEndBtn, paymentSection, endSection);

// Popup - Encerramento
endBtn.addEventListener("click", function () {
  modal.close();
  changeSection(endSection, pricingSection);
});