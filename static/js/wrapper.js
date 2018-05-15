function onTapSearchBtn() {
    var val =  isPC() ? $('#search-keyword').val() : $('.mobile-search-input').val()
    var domain = document.domain
    if (val == '' && searchKeyword() == undefined) {
        return
    }

    if (val != '') {
        window.location.href = '//' + domain + '/search/' + val
        return
    }

    window.location.href = '//' + domain
}

$(function () {
    if (!isPC()) {
        $('.col-md-4').remove()
        $('.pc-header').remove()
        $('.news-container').css('margin-top', '0px')
        $('.mobile-mark-div').css('min-height', '80px')
        $('.mobile-header').css('visibility', 'visible')
    } else {
        $('.mobile-header').remove()
        $('.mobile-mark-div').remove()
        $('.pc-header').css('visibility', 'visible')
    }

    $('.mobile-search-input').focus(function () {
        $('.mobile-search-input').css('background-color', '#fff')
        $('.mobile-btn-search').hide('200')
    })

    $('.mobile-search-input').blur(function () {
        $('.mobile-search-input').css('background-color', '#FFEEEE')
        $('.mobile-btn-search').show('200')
        setTimeout('onTapSearchBtn()', 500)
    })
})