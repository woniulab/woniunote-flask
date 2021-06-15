// 显示模态框中的登录面板
function showLogin() {
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

//  显示模态框中的注册面板
function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

//  显示模态框中的找回密码面板
function showReset() {
    $("#login").removeClass("active");
    $("#reg").removeClass("active");
    $("#find").addClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").addClass("active");
    $('#mymodal').modal('show');
}

function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    // 对邮箱地址进行校验(xxx@xxx.xx)
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确."});
        $("#regname").focus();
        return false;
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
             bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确."});
            $("#regname").focus();
            return false;
        }
        if (data == 'send-pass') {
            bootbox.alert({title:"信息提示", message:"邮箱验证码已成功发送，请查收."});
            $("#regname").attr('disabled', true);   // 验证码发送完成后禁止修改注册邮箱
            $(obj).attr('disabled', true);     // 发送邮件按钮变成不可用
            return false;
        }
        else {
            bootbox.alert({title:"错误提示", message:"邮箱验证码未发送成功."});
            return false;
        }
    })
}

function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {
        bootbox.alert({title:"错误提示", message:"注册邮箱不正确或密码少于5位."});
        return false;
    }
    else {
        // 构建POST请求的正文数据
        param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/user', param, function (data) {
            if (data == "ecode-error") {
                bootbox.alert({title:"错误提示", message:"验证码无效."});
                $("#regcode").val('');  // 清除验证码框的值
                $("#regcode").focus();   // 让验证码框获取到焦点供用户输入
            }
            else if (data == "up-invalid") {
                bootbox.alert({title:"错误提示", message:"注册邮箱不正确或密码少于5位."});
            }
            else if (data == "user-repeated") {
                bootbox.alert({title:"错误提示", message:"该用户名已经被注册."});
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                bootbox.alert({title:"信息提示", message:"恭喜你，注册成功."});
                // 注册成功后，延迟1秒钟重新刷新当前页面即可
                setTimeout('location.reload();', 1000);

            }
            else if (data == "reg-fail") {
                bootbox.alert({title:"错误提示", message:"注册失败，请联系管理员."});
            }
        });
    }
}

function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());

    if (loginname.length < 5 || loginpass.length < 5) {
        bootbox.alert({title:"错误提示", message:"用户名和密码少于5位."});
        return false;
    }
    else {
        // 构建POST请求的正文数据
        var param = "username=" + loginname;
        param += "&password=" + loginpass;
        param += "&vcode=" + logincode;
        // 利用jQuery框架发送POST请求，并获取到后台登录接口的响应内容
        $.post('/login', param, function (data) {
            if (data == "vcode-error") {
                bootbox.alert({title:"错误提示", message:"验证码无效."});
                $("#logincode").val('');  // 清除验证码框的值
                $("#logincode").focus();   // 让验证码框获取到焦点供用户输入
            }
            else if (data == "login-pass") {
                bootbox.alert({title:"信息提示", message:"恭喜你，登录成功."});
                // 注册成功后，延迟1秒钟重新刷新当前页面即可
                setTimeout('location.reload();', 1000);

            }
            else if (data == "login-fail") {
                bootbox.alert({title:"错误提示", message:"登录失败，请联系管理员."});
            }
        });
    }
}


// $(document).ready()是指页面加载即运行该代码
$(document).ready(function () {
    $.get('/loginfo', function (data) {
        content = '';
        if (data == null) {
            content += '<a class="nav-item nav-link" href="#" onclick="showLogin()">登录</a>';
            content += '<a class="nav-item nav-link" href="#" onclick="showReg()">注册</a>';
        }
        else {
            content += '<a class="nav-item nav-link" href="/ucenter">欢迎你：' + data["nickname"] + '</a>&nbsp;&nbsp;&nbsp;';
            if (data['role'] == 'admin') {
                content += '<a class="nav-item nav-link" href="/admin">系统管理</a>&nbsp;&nbsp;&nbsp;';
            }
            else {
                content += '<a class="nav-item nav-link" href="/ucenter">用户中心</a>&nbsp;&nbsp;&nbsp;';
            }
            content += '<a class="nav-item nav-link" href="/logout">注销</a>';
        }
        $("#loginmenu").append(content);
    });
});
