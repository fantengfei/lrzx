$(function () {
    // 编辑器
    var E = window.wangEditor
    var editor = new E('#editor')
    editor.create()

    var domain = document.domain

    $('.analysis-btn').click(function () {
        var btn = $(this).button('loading')

        var path = $('#url-input').val()
        if (path.length < 5) {
            return
        }

        var url = '//' + domain + '/analysis'
        $.post(url, {
            'url': path
        }, function (re) {
            var data = JSON.parse(re)
            var content = data['content'].substring('<html><body>'.length, data['content'].length - '</html></body>'.length)
            $('#article-title').val(data['title'])
            editor.txt.html(content)

            btn.button('reset')
        })
    })


    $('.post-btn').click(function () {
        var btn = $(this).button('loading')

        var title = $('#article-title').val()
        var conetent = editor.txt.html()

        var url = '//' + domain + '/post'


        btn.button('reset')
    })
})