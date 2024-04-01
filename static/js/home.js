window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('pagina')) {
        document.getElementById('section-2').scrollIntoView();
    }
};