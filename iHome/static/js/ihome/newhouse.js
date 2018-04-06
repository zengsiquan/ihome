function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/1.0/areas', function (response) {
        if (response.errno == '0') {
            // 渲染城区信息 <option value="1">东城区</option>
            $.each(response.data,function (i, area) {
                //console.log(area.aname)
                $('#area-id').append('<option value="'+area.aid+'">'+area.aname+'</option>');
            });
        } else {
            alert(response.errmsg);
        }
    });
    // TODO: 处理房屋基本信息提交的表单数据

    // TODO: 处理图片表单的数据

});