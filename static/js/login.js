$(function () {

    // 登录
    $('#login-button').click(function () {
        var username = $('#username').val()
        var password = $('#password').val()

        if (username.length < 10 || password.length < 5) {
            return
        }

        var domain = document.domain

        $('.login-tip').text('')
        $('.login-tip').append('<img class="login-loading" src="//' + domain + '/static/img/loading.gif" />')

        var url = '//' + domain + '/login'

        $.post(url, {
            'username': username,
            'password': password
        }, function (re) {
            $('.login-loading').remove()
            if (re != 'success') {
                $('.login-tip').text(re)
                return
            }

            location.href = '/post'
        })
    })
})