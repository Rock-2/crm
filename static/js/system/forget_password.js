/**
 * Created by 磊 on 2018/10/27.
 */

//验证用户名是否唯一
function forget_username() {
    var flag = false;
    //获取用户名
    var username = $('#system_forget_username').val().trim();
    // 非空判断
    if (undefined == username || '' == username) {
        $('#username_span').html('用户名不能为空');
        return flag;
    }

    //合法后清空提示信息
    $('#username_span').html('');
    //发送ajax请求
    $.ajax({
        type: 'POST',
        url: '/system/forget_username/',
        //将ajax异步改为同步
        async: false,

        data: {
            //防止csrf保护机制拦截
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username
        },
        dataType: 'json',
        success: function (result) {
           console.log(result);
            if (200 == result.code) {
                flag = true;
                $('#username_span').html(result.msg)
            }
            if (400 == result.code) {
                flag = false;
                 $('#username_span').html(result.msg)
            }

        },
        error: function (result) {
            console.log(result);
        }
    });
    return flag;
}
//丢失焦点,触发事件
$('#system_forget_username').on('blur', forget_username);

//验证邮箱格式
function forget_email() {
    var flag = false;
    //获取邮箱
    var email = $('#system_forget_email').val().trim();
    // 非空判断
    if (undefined == email || '' == email) {
        $('#email_span2').html('邮箱不能为空');
        return flag;
    }
    //合法后清空提示信息
    $('#email_span2').html('');
    //发送ajax请求
    $.ajax({
        type: 'POST',
        url: '/system/forget_email/',
        //将ajax异步改为同步
        async: false,

        data: {
            //防止csrf保护机制拦截
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email
        },
        dataType: 'json',
        success: function (result) {
            console.log(result);
            if (200 == result.code) {
                flag = true;
                $('#email_span2').html(result.msg)
            }
            if (400 == result.code) {
                flag = false;
                 $('#email_span2').html(result.msg)
            }

        },
        error: function (result) {
            console.log(result);
        }
    });
    return flag;
}
//丢失焦点,触发事件
$('#system_forget_email').on('blur', forget_email);


// 点击注册按钮再次验证数据合法性
$('#system_forget_btn').on('click', function () {
    // 点击注册以后置灰按钮
    $('#system_forget_btn').attr("disabled", "true");

    //合法的话  发送邮件激活邮箱
    // 获取用户名
    var username = $('#system_forget_username').val();
    // 获取邮箱
    var email = $('#system_forget_email').val().trim();


    $.ajax({
        type: 'POST',
        url: '/system/send_email2/',
        async: false,
        data: {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email,
            'username': username

        },
        dataType: 'json',
        success: function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#username_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#username_span').html(result.msg);
            }
        },
        error: function (result) {
            console.log(result);
        }
    });

});
//--------------------------------------修改密码---------------------------------
//验证密码
function verify_password2() {
    //获取密码
    var pwd = $('#system_update_pwd2').val();
    //验证密码
    var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
    // 非空判断
    if (undefined == pwd || '' == pwd) {
        $('#pwd_span5').html('重复密码不能为空');
        return false;
    }
    if (!reg.test(pwd)) {
        $('#pwd_span5').html('请输入8-16位字符,');
        return false
    }

    //合法后清空提示
    $('#pwd_span5').html('');
    return true;
}
$('#system_update_pwd2').on('blur', verify_password2);

//判断重复密码
function verify_password3() {
    //获取密码
    var pwd = $('#system_update_pwd2').val();
    var pwd2 = $('#system_update_pwd3').val();
    // 非空判断
    if (undefined == pwd2 || '' == pwd2) {
        $('#pwd_span6').html('重复密码不能为空');
        return false;
    }
    //进行比较
    if (pwd2 != pwd) {
        $('#pwd_span5').html('两次密码不一致');
        return false
    }
    //合法后清空提示
    $('#pwd_span6').html('');
    return true
}
$('#system_update_pwd3').on('blur', verify_password3);


// 点击注册按钮再次验证数据合法性
$('#system_update_btn').on('click', function () {
    // 点击注册以后置灰按钮
    $('#system_update_btn').attr("disabled", "true");

    //合法的话  获取密码
    // 获取用户名
    var pwd1 = $('#system_update_pwd').val();
    // 获取邮箱
    var pwd2 = $('#system_update_pwd2').val().trim();


    $.ajax({
        type: 'POST',
        url: '/system/system_update_btn/',
        async: false,
        data: {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'pwd1': pwd1,
            'pwd2': pwd2

        },
        dataType: 'json',
        success: function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#pwd_span5').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#pwd_span5').html(result.msg);
            }
        },
        error: function (result) {
            console.log(result);
        }
    });

});





//--------------------------------------修改密码---------------------------------