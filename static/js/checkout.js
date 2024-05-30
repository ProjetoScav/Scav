const stripe = Stripe(
  "pk_test_51PDnRKI0MO5skub5kx17A9PGZU1TBEuszP9nrofdo2PLfxggXI6fnQ3GH0LKoKfG1pC9KT2VVkkgsk9vG6UmtrqG007pRQBIuQ"
);

let elements;

initialize();
checkStatus();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);
