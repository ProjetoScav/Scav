"strict";
// Validação de email
// Expressão regular para validar o formato do e-mail
function validateEmail(email) {
  var emailRegex =
    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return emailRegex.test(email);
}

// Eventos do input
inputEmail = document.querySelector(".payment__email");
let isEmail = false;
inputEmail.addEventListener("keydown", function (e) {
  const email = inputEmail.value;
  isEmail = validateEmail(email);
  if (e.keyCode === 13) {
    e.preventDefault();
    toEndBtn.click();
  }
});

inputEmail.addEventListener("input", function () {
  isEmail = validateEmail(inputEmail.value);
});

// Formulário - Remoção de valores inválidos
const dddInput = document.querySelector("#ddd");
const cepInput = document.querySelector("#cep");
const cpAteInput = document.querySelector("#capital_social_ate");
const cpDesdeInput = document.querySelector("#capital_social_desde");
const ufInput = document.querySelector("#uf");
const cidadeInput = document.querySelector("#municipio");
// const bairroInput = document.querySelector("#capital_social_desde");

const removeLetters = function (input) {
  input.addEventListener("input", function () {
    input.value = input.value.replace(/(?![0-9, ])./gim, "");
  });
};

const removeNonNumeric = function (input) {
  input.addEventListener("input", function () {
    input.value = input.value.replace(/(?![0-9])./gim, "");
  });
};

const removeNumeric = function (input) {
  input.addEventListener("input", function () {
    input.value = input.value.replace(/(?![A-zÀ-ú\s,])./gim, "");
  });
};

removeLetters(dddInput);
removeLetters(cepInput);
removeNonNumeric(cpAteInput);
removeNonNumeric(cpDesdeInput);
removeNumeric(ufInput);
removeNumeric(cidadeInput);

// Função
const inputsForm = document.querySelectorAll("#form input");
const form = document.querySelector("#form");

const preventEnter = function (element) {
  element.addEventListener("keydown", function (e) {
    if (e.keyCode === 13) {
      e.preventDefault();
    }
  });
};

inputsForm.forEach(preventEnter);
preventEnter(form);
