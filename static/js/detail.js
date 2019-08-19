$(function () {
    var referer = document.referrer
    if (referer.indexOf(document.domain) == -1 && !isPC()) {
        $('.bottom-guide-wrapper').css('visibility', 'visible')
    }
})