$(document).ready(function () {
    var deviceWidth = $(window).width() > 450 ? 450 : $(window).width()
    if (isPC()) {
        deviceWidth = 450
    }

    var pixels = (deviceWidth / 4.5) + "px"

    var css = {
        'font-size': pixels
    }

    $("#wrapper-html").css(css)

    // detail.html font-size
    $(".content-db p").css('font-size', isPC() ? 0.17+'rem' : 0.2+'rem')


    $(".full-info-container").hover(function (e) {
        var target = $(e.target).prev().children('.full-img-layout')
        target.css('-webkit-transform', 'scale(1.05)')
    }, function (e) {
        var target = $(e.target).prev().children('.full-img-layout')
        target.css('-webkit-transform', 'scale(1.0)')
    })
})