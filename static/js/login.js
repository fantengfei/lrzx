$(function () {

    // 登录
    $('#login-button').click(function () {
        var username = $('#username').val()
        var password = $('#password').val()

        if (username.length < 10 || password.length < 5) {
            return
        }

        var btn = $(this).button('loading');

        var domain = document.domain

        $('.login-tip').text('')

        var url = '//' + domain + '/login'

        $.post(url, {
            'username': username,
            'password': password
        }, function (re) {
            btn.button('reset')

            if (re != 'success') {
                $('.login-tip').text(re)
                return
            }

            location.href = '/post'
        })
    })
})