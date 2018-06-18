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
    
    $('.post-category').click(function () {
        var id = $(this).attr('id')
        $('.dropdown-toggle').attr('id', 'menu-' + id)
        $('.dropdown-toggle b').html($(this).text())
    })


    $('.post-btn').click(function () {
        var id = $('.dropdown-toggle').attr('id')
        var title = $('#article-title').val()
        var content = editor.txt.html()
        var imgs = ""

        $('#editor img').each(function(){
            imgs = imgs + "," + $(this).attr("src")
        });

        if (title == undefined || content == undefined || id == undefined) {
            return
        }

        var btn = $(this).button('loading')

        var url = '//' + domain + '/post'
        $.post(url, {
            'title': title,
            'content': content,
            'imgs': imgs,
            'type': id.charAt(id.length - 1)
        }, function (e) {
            btn.button('reset')

            if (e != 'failure') {
                location.href = '/detail/' + e
                return
            }

            alert('发布失败，请检查内容后再试～')
        })


    })
})