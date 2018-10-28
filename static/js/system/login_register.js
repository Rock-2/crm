/**
 * Created by 磊 on 2018/10/25.
 */
//点击注册显示注册div,隐藏登录div
$('#reg_a').on('click', function () {
    $('#log-in').hide();
    $('#register').show();
});
//点击登录显示登录页面div
$('#log_a').on('click', function () {
    //先隐藏后展示
    $('#register').hide();
    $('#log-in').show();
});
//验证用户名,必须字母加数字
function verify_username() {
    var flag = false;
    //获取用户名
    var username = $('#reg_username').val();
    //验证用户名必须是字母加数字
    //      var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{4,16}$/
    var reg = /^[A-Za-z0-9]{4,16}$/;
    // 非空判断
    if (undefined == username || '' == username) {
        $('#reg_span').html('用户名不能为空');
        return flag;
    }
    if (!reg.test(username)) {
        $('#reg_span').html('请输入4-16位字母和数字的组合');
        return flag;
    }
    //合法后清空提示信息
    $('#reg_span').html('');
    //发送ajax请求
    $.ajax({
        type: 'POST',
        url: '/system/verify_username/',
        //将ajax异步改为同步
        async: false,

        data: {
            //防止csrf保护机制拦截
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username
        },
        dataType: 'json',
        success: function (result) {
            if (400 == result.code) {
                flag = false;
                $('#reg_span').html(result.msg)
            }
            if (200 == result.code) {
                flag = true;

            }

        },
        error: function (result) {
            console.log(result);
        }
    });
    return flag;

}
//丢失焦点事件
$('#reg_username').on('blur', verify_username);
//验证邮箱格式
function verify_email() {
    var flag = false;
    //获取用户名
    var email = $('#reg_email').val().trim();
    // 非空判断
    if (undefined == email || '' == email) {
        $('#email_span').html('邮箱不能为空');
        return flag;
    }
    //验证用户名必须是字母加数字
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;

    if (!reg.test(email)) {
        $('#email_span').html('请输入正确的邮箱格式');
        return flag;
    }
    //合法后清空提示信息
    $('#email_span').html('');
    //发送ajax请求
    $.ajax({
        type: 'POST',
        url: '/system/verify_email/',
        //将ajax异步改为同步
        async: false,

        data: {
            //防止csrf保护机制拦截
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email
        },
        dataType: 'json',
        success: function (result) {
            if (400 == result.code) {
                flag = false;
                $('#email_span').html(result.msg)
            }
            if (200 == result.code) {
                flag = true;

            }

        },
        error: function (result) {
            console.log(result);
        }
    });
    return flag;
}
//丢失焦点,触发事件
$('#reg_email').on('blur', verify_email);
//验证密码
function verify_password() {
    //获取密码
    var pwd = $('#password1').val();
    //验证密码
    var reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
    // 非空判断
    if (undefined == pwd || '' == pwd) {
        $('#pwd_span').html('重复密码不能为空');
        return false;
    }
    if (!reg.test(pwd)) {
        $('#pwd_span').html('请输入8-16位字符,');
        return false
    }

    //合法后清空提示
    $('#pwd_span').html('');
    return true;
}
$('#password1').on('blur', verify_password);

//判断重复密码
function verify_password2() {
    //获取密码
    var pwd = $('#password1').val();
    var pwd2 = $('#password2').val();
    // 非空判断
    if (undefined == pwd2 || '' == pwd2) {
        $('#pwd_span2').html('重复密码不能为空');
        return false;
    }
    //进行比较
    if (pwd2 != pwd) {
        $('#pwd_span2').html('两次密码不一致');
        return false
    }
    //合法后清空提示
    $('#pwd_span2').html('');
    return true
}
$('#password2').on('blur', verify_password2);
// 点击注册按钮再次验证数据合法性
$('#reg_btn').on('click', function () {
    // 点击注册以后置灰按钮
    $('#reg_btn').attr("disabled", "true");

    var flag = verify_username();
    if (!flag) {
        return;
    }
    var flag = verify_email();
    if (!flag) {
        return;
    }
    var flag = verify_password();
    if (!flag) {
        return;
    }
    var flag = verify_password2();
    if (!flag) {
        return;
    }
    //合法的话  发送邮件激活邮箱
    // 获取用户名
    var username = $('#reg_username').val();
    // 获取邮箱
    var email = $('#reg_email').val().trim();
    // 获取密码
    var password = $('#password2').val();

    $.ajax({
        type: 'POST',
        url: '/system/send_email/',
        async: false,
        data: {
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'email': email,
            'username': username,
            'password': password
        },
        dataType: 'json',
        success: function (result) {
            // 如果是400 设置为false返回
            if (400 == result.code) {
                $('#reg_span').html(result.msg);
            }

            // 如果是200 正常显示
            if (200 == result.code) {
                $('#reg_span').html(result.msg);
            }
        },
        error: function (result) {
            console.log(result);
        }
    });

});
//--------------------------------------登录----------------------------------
//用户名非空验证
function login_verify_username() {
    //获取用户名
    var username = $('#log_username').val().trim();
    // 非空判断
    if (undefined == username || '' == username) {
        $('#log_span').html('请输入用户名');
        return false;

    }
    //合法后清空提示信息
    $('#log_span').html('');
        return true;

}
//丢失焦点事件
$('#log_username').on('blur', login_verify_username);
//密码非空验证
function login_verify_password() {
    //获取密码
    var password = $('#log_password').val().trim();
    // 非空判断
    if (undefined == password || '' == password) {
        $('#log_span').html('请输入密码');
            return false;

    }
    //合法后清空提示信息
    $('#log_span').html('');
        return true;

}
//丢失焦点事件
$('#log_password').on('blur', login_verify_password);
//登录
function login_user() {
    var flag = login_verify_username();
    if (!flag)
        return;
    flag = login_verify_password();
    if (!flag)
        return;
     // 判断是否选择了记住密码
    var remember = $('#remember').is    (':checked');
    var username = $('#log_username').val().trim();
    var password = $('#log_password').val().trim();

    //发送ajax请求
    $.ajax({
        type: 'POST',
        url: '/system/login_user/',
        //将ajax异步改为同步
        async: false,

        data: {
            //防止csrf保护机制拦截
            'csrfmiddlewaretoken': $.cookie('csrftoken'),
            'username': username,
            'password': password,
            'remember':remember
        },
        dataType: 'json',
        success: function (result) {
            if (400 == result.code) {

                $('#log_span').html(result.msg)
            }
            if (200 == result.code) {
                 // 如果用户选择了记住密码
                if (!(undefined == result.login_username_cookie || null == result.login_username_cookie)) {
                    // 设置cookie，有效时间为5天
                    $.cookie('login_username_cookie', result.login_username_cookie,
                        {'expires': 5, 'path': '/', 'domain': '127.0.0.1'});

                    $.cookie('login_password_cookie', result.login_password_cookie,
                        {'expires': 5, 'path': '/', 'domain': '127.0.0.1'});
                }
                window.location.href = '/system/index/'
            }

        },
        error: function (result) {
            console.log(result);
        }
    });

}
$('#login_btn').on('click', login_user);
//进入页面就执行的方法,实现免登陆
$(function () {
    //获取到login_cookie,赋值到登录框
     var username = $.cookie('login_username_cookie');
    var password = $.cookie('login_password_cookie');
    // 判断是否存在cookie
    if (!(undefined == username || null == username)) {
        // base64解密cookie
        username = $.base64.decode(username);
        // 赋值到登录框
        $('#login_username').val(username);
    }

    if (!(undefined == password || null == password)) {
        // base64解密cookie
        password = $.base64.decode(password);
        // 赋值到登录框
        $('#login_password').val(password);
    }

});

//忘记密码
function forget_password() {
    // window.location.href = '/system/forget_password/'
}
// $('#forget_password').on('click', forget_password);






//--------------------------------------登录----------------------------------



