//Define a direção da seta no carregamento
var sideBarMargin = parseInt($('#sidebar').css("margin-left"));
switch(sideBarMargin) {
    case -0:
        $('#arowButton').toggleClass('fa-angle-left');
        break;
    case -160:
        $('#arowButton').toggleClass('fa-angle-right');
        break;
    } 

//Ao clicar na seta muda a sidebar e a seta
jQuery(document).ready(function($){
    sideBarMargin = parseInt($('#sidebar').css("margin-left"));
    
    $('#sidebarCollapse').on('click', function () {
        toogleSideBar()
    });
    $('#sidebarReturn').on('click', function () {
        toogleSideBar()
    });
});

//função que realiza a modificação na seta e verifica a margem da sidebar
function toogleSideBar(){
    $('#sidebarColapssed').toggleClass('active');
        $('#sidebar').toggleClass('active');
        sideBarMargin = parseInt($('#sidebar').css("margin-left"));

        switch(sideBarMargin) {
            case 0:
                $('#arowButton').addClass('fa-angle-right');
                $('#arowButton').removeClass('fa-angle-left');
                break;
            case -160:
                $('#arowButton').addClass('fa-angle-left');
                $('#arowButton').removeClass('fa-angle-right');
                break;
            } 
}
/*
window.onresize  = function(){
    if( $(window).width() <= 768){
        $('#arowButton').addClass('fa-arrow-right');
        $('#arowButton').removeClass('fa-arrow-left');
    }
    else ( $(window).width() >= 768);
        $('#arowButton').addClass('fa-arrow-left');
        $('#arowButton').removeClass('fa-arrow-right');
}*/

