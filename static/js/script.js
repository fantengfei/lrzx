// 网页抓取工具

function yidianzixun(url, host) {
    var webPage = require('webpage')
    var page = webPage.create()
    var count = 0
    var repeate = 0

    page.viewportSize = { width: 1920, height: 1080 };
    page.open(url, function() {
        page.includeJs('https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js', function() {
            var evaluate = function () {
                var re = page.evaluate(function () {
                    window.scrollTo(0, $(document).height())
                    return $('html').html()
                })
                console.log(re.length)
                return re.length
            }

            count = evaluate()

            var logic = function () {
                var a = setTimeout(function () {
                    var amout = evaluate()
                    if (69540 > count) {
                        console.log('网页抓取中...')
                        count = amout
                        logic()
                    } else {
                        if (repeate < 3) {
                            repeate = repeate + 1
                            logic()
                            return
                        }

                        console.log('end\n---------------------------------------------------------------')
                        phantom.exit()
                    }
                }, 1000)
            }

            logic()
        })
    })
}

yidianzixun('https://www.yidianzixun.com/channel/w/%E6%9C%88%E7%BB%8F', 'www.yidianzixun.com')