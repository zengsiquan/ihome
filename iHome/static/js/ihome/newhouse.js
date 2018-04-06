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
    $('#form-house-info').submit(function (event) {
        event.preventDefault();
        var params={};
        $(this).serializeArray().map(function (obj) {
            params[obj.name] = obj.value;
        });
        // 收集房屋设施信息
        facilities = [];
        $(':checkbox:checked[name=facility]').each(function (i,elem){
            facilities[i] = elem.value;
        });
        params['facility'] = facilities;
        $.ajax({
            url:'/api/1.0/houses',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno == '0'){
                    $('#form-house-info').hide()
                    $('#form-house-image').show()
                } else if (response.errno == '4101') {
                    location.href = '/';
                } else {
                    alert(response.errmsg)
                }
            }
        });

    });
    // TODO: 处理图片表单的数据

});