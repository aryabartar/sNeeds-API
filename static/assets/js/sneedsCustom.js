function clearAdvancedSearchForm() {
    var myFormElement = document.getElementById("sneedsAdvancedSearchForm");
    var elements = myFormElement.elements;

    // var temp = "0";
    // var mySelect = document.getElementById("categorySearchSelector");
    //
    // for(var i, j = 0; i = mySelect.options[j]; j++) {
    //     if(i.value == temp) {
    //         mySelect.selectedIndex = j;
    //         break;
    //     }
    // }

    for (i = 0; i < elements.length; i++) {

        field_type = elements[i].type.toLowerCase();

        switch (field_type) {

            case "text":
            case "password":
            case "textarea":
            case "hidden":

                elements[i].value = "";
                break;

            case "radio":
            case "checkbox":
                if (elements[i].checked) {
                    elements[i].checked = false;
                }
                break;

            case "select-one":
            case "select-multi":

                break;
            default:
                break;
        }
    }
}

$("#goUpBtn").click(function () {
    scrollTo(0, 0);
});


var topNavElement = $("nav.navbar-fixed-top");
var activeListItemLink = topNavElement.find("ul.nav li.active > a");

(function () {
    // console.log("scroll X : " + scrollX + "\nScroll Y : " + scrollY);
    if (scrollY >= 50) {
        topNavElement.removeClass("navbar-transparent").addClass("navbar-default");
        activeListItemLink.addClass("activeLinkNewBgColor").removeClass("activeLinkOldBgColor");
    } else {
        topNavElement.removeClass("navbar-default").addClass("navbar-transparent");
        activeListItemLink.removeClass("activeLinkNewBgColor").addClass("activeLinkOldBgColor");
    }
    var docWidth = document.body.offsetWidth;
    // console.log("document width:" + docWidth);
    var registerElement = $("#signUpCard");

    if (docWidth <= 974) {
        // console.log("asghar")
        if (!registerElement.hasClass("fixTopMarginForRegister")) {
            registerElement.addClass("fixTopMarginForRegister");
        }
    } else {
        if (registerElement.hasClass("fixTopMarginForRegister")) {
            registerElement.removeClass("fixTopMarginForRegister");
        }
    }

    setTimeout(arguments.callee, 500);
})


(function () {
    var inputElement = $("#siteFastSearch");
    if (inputElement.offsetTop < 200)
        inputElement.style.color = "white";
    else
        inputElement.style.color = "gray";
    setTimeout(arguments.callee, 1000);
});

$(document).ready(function(){
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});