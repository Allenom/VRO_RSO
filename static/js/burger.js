$(document).ready(function () {
    let headerBurger = $(".menu-burger__header");
    let headerBurgerMenu = $(".menu-burger__header + .header__nav");
    let imgBurger = $(".menu-burger_img");
    let imgBurgerMenu = $(".menu-burger_img + .header__nav");
    let imgActive = $(".avatar_img");
    let accorCheckbox = $(".acor-container input[type=checkbox]");
    headerBurger.on("click", function () {
        if (headerBurger.hasClass("open-menu")) {
            $("body").removeClass("fixed-page");
            accorCheckbox.prop('checked', false);
        } else {
            $("body").addClass("fixed-page");
        }
        $(this).toggleClass("open-menu");
        headerBurgerMenu.toggleClass("open-menu");
        imgBurger.removeClass("open-img");
        imgBurgerMenu.removeClass("open-img");
        imgActive.removeClass("img_active");
    });

    imgBurger.on("click", function () {
        if (imgBurger.hasClass("open-img")) {
            $("body").removeClass("fixed-page");
        } else {
            $("body").addClass("fixed-page");
        }
        $(this).toggleClass("open-img");
        imgBurgerMenu.toggleClass("open-img");
        headerBurger.removeClass("open-menu");
        headerBurgerMenu.removeClass("open-menu");
        imgActive.toggleClass("img_active");
    });
});


