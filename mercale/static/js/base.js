//função jquery que apaga qualquer alerta que surgir na tela após 2 segundos, usando um fadeOut para remover a tela
window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 2000);