$(function () {
    var pcHeight = {'height': '230px'}
    var mobileHeight = {'height': '150px'}
    if (isPC()) {
        $('.banner-container').css(pcHeight)
        $('.banner-item-container').css(pcHeight)
        $('.banner-item-image').css(pcHeight)
    } else {
        $('.banner-container').css(mobileHeight)
        $('.banner-item-container').css(mobileHeight)
        $('.banner-item-image').css(mobileHeight)
    }



    var visbile = {'visibility': 'visible'}
    var hidden = {'visibility': 'hidden'}

    $('.banner-bottom-mark').css(hidden)
    $('#banner-mark-1').css(visbile)

    $('.banner-item-container').hide()
    $('#banner-item-1').show()
    $('#banner-item-1').addClass('banner-item-current')

    setInterval(function () {
        change()
    }, 5000)


    $('.banner-switch-right').hover(function () {
        $('.banner-switch-right i').addClass('icon-right')
    }, function () {
        $('.banner-switch-right i').removeClass('icon-right')
    })

    $('.banner-switch-left').hover(function () {
        $('.banner-switch-left i').addClass('icon-left')
    }, function () {
        $('.banner-switch-left i').removeClass('icon-left')
    })

    $('.banner-switch-right').click(function () {
        change()
    })

    $('.banner-switch-left').click(function () {
        change(1)
    })


    // 0 : 表示下一个 1: 表示上一个
    function change(direction = 0) {
        var current = $('.banner-item-current')
        var cId = current.attr('id')
        var index = cId.slice(cId.length - 1)

        index = parseInt(index) + (direction ? -1 : 1)
        current.removeClass('banner-item-current')

        var nextObj = $('#banner-item-' + index)

        if (nextObj.length <= 0) {
            if (direction) {
                var items = $('.banner-item-container')
                nextObj = $(items[items.length - 1])
                var id =  nextObj.attr('id')
                index = id.slice(id.length - 1)
            } else {
                nextObj = $('#banner-item-1')
                index = 1
            }
        }

        nextObj.addClass('banner-item-current')

        current.fadeOut(600)
        nextObj.fadeIn(600)

        $('.banner-bottom-mark').css(hidden)
        $('#banner-mark-' + index).css(visbile)
    }
})