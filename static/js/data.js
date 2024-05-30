document.addEventListener("alpine:init", () => {
  console.log("bolado");
  Alpine.store("pedido", {
    termo: "",
    atividade_principal: "",
    incluir_atividade_secundaria: "",
    natureza_juridica: "",
    situacao_cadastral: "2",
    uf: "",
    municipio: "",
    bairro: "",
    cep: "",
    ddd: "",
    data_abertura_desde: "",
    data_abertura_ate: "",
    capital_social_desde: "",
    capital_social_ate: "",
    somente_mei: "",
    somente_matriz: "",
    com_contato_telefonico: "",
    somente_fixo: "",
    com_email: "",
    excluir_mei: "",
    somente_filial: "",
    somente_celular: "",
  });
});
