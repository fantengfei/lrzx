$(document).ready(function () {
    var deviceWidth = $(window).width() > 450 ? 450 : $(window).width()
    if (isPC()) {
        deviceWidth = 450
    }

    var pixels = (deviceWidth / 4.5) + "px"

    var css = {
        'font-size': pixels,
        'height': pixels,
        'max-height': pixels,
        'min-height': pixels,
        'line-height': pixels,
        'width': '100%',
        'max-width': '100%',
        'min-width': '100%'
    }

    $("#wrapper-html").css(css)

    // detail.html font-size
    $(".content-db p").css('font-size', isPC() ? 0.17+'rem' : 0.2+'rem')

})