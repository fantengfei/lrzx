$(document).ready(function() {
    reload_cell_style()

    var keyword = searchKeyword()
    if (keyword != undefined) {
        $('#search-keyword').val(decodeURIComponent(keyword))
        $('.mobile-search-input').val(decodeURIComponent(keyword))
    }

    var list_loading = false
    var is_end = false
    
    $(document).scroll(function () {
        var mark_top = $('#news-container').offset().top + $('#news-container').height()
        var offset = $(window).height() + $(window).scrollTop()

        if (!list_loading && (offset >= mark_top) && !is_end) {
            load_more_msg()
        }

        var navTop = document.getElementsByClassName('header-layout-wrapper')[0].getBoundingClientRect().top
        if (navTop <= -105) {
            $('.nav-layout').addClass('navbar-fixed-top')
            $('.container-wrapper').css('margin-top', $('.nav-layout').height())
        } else {
            $('.nav-layout').removeClass('navbar-fixed-top')
            $('.container-wrapper').css('margin-top', '0px')
        }
    })


    function load_more_msg() {
        list_loading = true
        var target = $('#news-container')
        var domain = document.domain
        var offset = target.children().length

        var type = currentType()
        if (type != -1) {
            offset = type + '/' + offset
        }

        var keyword = searchKeyword()
        if (keyword != undefined) {
            offset = offset + '/' + keyword
        }

        $('.page_loading').remove()
        target.append('<div class="page_loading base-style"><img src="//' + domain + '/static/img/loading.gif" />加载中...</div>')
        $.get('//'+domain+'/load_more/' + offset).done(function(data) {
            target.append(data)
            reload_cell_style()
            if (data != '') {
                $('.page_loading').remove()
            } else {
                $('.page_loading').text('暂无更多内容')
                is_end = true
            }

            list_loading = false
        })
    }

    function reload_cell_style() {
        // macro.html img
        var width = isPC() ? '24%' : '32.7%'
        $('.img-multi-layout div').css({'min-width': width, 'max-width': width})
        $('.item-layout-a').attr('target',  isPC() ? '_blank' : '_self')


        // 分割线
        var height = isPC() ? '1px' : '0.5px'
        var color = isPC() ? '#f2f2f5' : '#ddd'
        $('.separate-div').css({'height': height, backgroundColor: color})
        $('.card-a-name').css('border-bottom', height + ' solid ' + color)
    }
    

})