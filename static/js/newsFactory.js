$(function () {
    // macro.html img
    var width = isPC() ? '24%' : '32.5%'
    $('.img-multi-layout div').css({'min-width': width, 'max-width': width})
    $('.item-layout-a').attr('target',  isPC() ? '_blank' : '_self')


    // 分割线
    var height = isPC() ? '1px' : '0.5px'
    var color = isPC() ? '#f2f2f5' : '#ddd'
    $('.separate-div').css({'height': height, backgroundColor: color})
    $('.card-a-name').css('border-bottom', height + ' solid ' + color)
})