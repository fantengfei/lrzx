function isPC(){
    var userAgentInfo = navigator.userAgent
    var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPod")
    var flag = true
    for (var v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
            flag = false
            break
        }
    }

    return flag
}

function searchKeyword() {
    var querys = window.location.pathname.split('/')
    var keyword = undefined
    for (var index in querys) {
        if (querys[index] == 'search') {
            keyword = querys[parseInt(index) + 1]
            break
        }
    }
    return keyword
}

function currentPathName() {
    var querys = window.location.pathname.split('/')
    var pathName = querys[1]
    return pathName
}

function currentType() {
    var type = -1
    switch (currentPathName()){
        case '': type = 1; break;
        case 'dayima': type = 1; break;
        case 'education': type = 2; break;
        case 'beiyun': type = 3; break;
        case 'meizhuang': type = 4; break;
        case 'health': type = 5; break;
    }
    return type
}