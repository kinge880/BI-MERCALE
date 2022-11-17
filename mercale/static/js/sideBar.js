//Define a direção da seta no carregamento
var sideBarMargin = parseInt($('#sidebar').css("margin-left"));
switch(sideBarMargin) {
    case -0:
        $('#arowButton').toggleClass('fa-angle-left');
        break;
    case -200:
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
                $('#sidebarColapssed').addClass('btn-close');
                $('#arowButton').removeClass('fa-angle-left');
                $('#sidebarColapssed').removeClass('btn-open');
                break;
            case -200:
                $('#arowButton').addClass('fa-angle-left');
                $('#sidebarColapssed').addClass('btn-open');
                $('#arowButton').removeClass('fa-angle-right');
                $('#sidebarColapssed').removeClass('btn-close');
                break;
            } 
}

$(document).ready(function() {
    var colors = ["#cd5c5c", '#ffff00'];//Array com as cores, pode adicionar contas quiser
    var i = 0;
    setInterval(function(){
      $('#nav_request_pendent').css('color', colors[i]);
      i = (i == (colors.length -1)) ? 0 : i+1;
    },800);//1 Segundo em Milisegundos
});

function clique(id){
    document.getElementById("home").style.display = "none";
    document.getElementById("notmobilebi").style.display = "none";
    document.getElementById("bimercale").style.display = "block";
    if (screen.width < 640 || screen.height < 480) {
        id = id+'mobile'
        var testButton = document.getElementById(id).getAttribute('href');
        
        if (testButton == ''){
            document.getElementById("home").style.display = "none";
            document.getElementById("notmobilebi").style.display = "block";
            document.getElementById("bimercale").style.display = "none";
        } else {
            var button = document.getElementById(id);
            button.click();
        }
    } else {
        var button = document.getElementById(id);
        button.click();
    }
}

function cliquehome(){
    document.getElementById("notmobilebi").style.display = "none";
    document.getElementById("bimercale").style.display = "none";
    document.getElementById("home").style.display = "block";
}

