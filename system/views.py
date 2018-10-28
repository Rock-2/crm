from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import User
from django.http import JsonResponse, HttpResponse
from email.header import Header  # 如果包含中文，需要通过Header对象进行编码
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib  # 负责发送邮件
import uuid
from datetime import datetime, timedelta
from hashlib import md5
import base64


# Create your views here.

# 跳转登录跟注册页面
def login_register(request):
    # # 判断session中是否有用户信息
    # username = request.session.get('username_session')
    # if username:
    #     return render(request, 'system/index.html')
    #
    # # 如果不存在，重定向登录页面
    # return redirect('system:login_register')

    return render(request, 'system/login.html')


# 验证用户名是否唯一
@require_POST
def verify_username(request):
    try:
        # 接收参数,
        username = request.POST.get('username')
        # 查询是否有该用户
        user = User.objects.get(username=username)
        # 有用户返回页面Json
        return JsonResponse({'code': 400, 'msg': '用户名已存在'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '恭喜你可以注册'})


@require_POST
def verify_email(request):
    try:
        # 接收参数
        email = request.POST.get('email')
        # 查询是否有该用户
        user = User.objects.get(email=email)
        # 有用户返回页面json
        return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '恭喜你可以注册'})


        # -----------------发送邮件验证--------------#
        # 构建一个格式化邮箱地址的函数


def format_addr(s):
    name, addr = parseaddr(s)  # 将我们的邮箱地址字符串拆分为name,addr
    name = Header(name, 'utf-8')  # 因为name可能是汉字 需要编码
    return formataddr((str(name), addr), 'utf-8')  # 格式化邮箱并返回


@require_POST
def send_email(request):
    # 发件人邮箱
    send_email = 'm15171636873@163.com'
    # 授权码
    passworld = 'ly1207'

    # 邮件发送的服务器地址
    email_server = 'smtp.163.com'
    # 收件人邮箱
    to_addr = request.POST.get('email')
    # 用户名
    username = request.POST.get('username')
    # 用户密码
    u_pwd = request.POST.get('password')
    # print(type(u_pwd))
    # 使用md5加密
    u_pwd = md5(u_pwd.encode(encoding='utf-8')).hexdigest()
    # print(type(u_pwd))
    # 激活码
    code = ''.join(str(uuid.uuid4()).split('-'))
    # 10分钟后的时间戳
    td = timedelta(minutes=10)
    ts = datetime.now() + td
    ts = str(ts.timestamp()).split('.')[0]
    # 插入数据库
    user = User(username=username, password=u_pwd, email=to_addr, code=code, timestamp=ts)
    user.save()
    html = """
        <html>
            <body>
                <div>
                Email 地址验证<br>
                这封信是由 上海尚学堂 发送的。<br>
                您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br>
                如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                ----------------------------------------------------------------------<br>
                 帐号激活说明<br>
                ----------------------------------------------------------------------<br>
                如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                您只需点击下面的链接激活帐号即可：<br>
                <a href="http://127.0.0.1:8000/system/active_accounts/?username={}&code={}&timestamp={}">http://www.crm.com/active_accounts/?username={}&amp;code={}&amp;timestamp={}</a><br/>
                感谢您的访问，祝您生活愉快！<br>
                此致<br>
                 上海尚学堂 管理团队.
                </div>
            </body>
        </html>""".format(username, code, ts, username, code, ts)
    msg = MIMEText(html, "html", "utf-8")
    '''
        构建邮件内容对象
            第一个参数是邮件内容
            第二个参数是MIME，必须是plain即text/plain否则中文不显示
            第三个参数是编码
    '''

    # 标准邮件需要三个头部信息：From To 和 Subject
    # 设置发件人和收件人的信息
    # 比如：尚学堂 <java_mail01@163.com>
    # 发件人
    msg['From'] = format_addr('CRM系统官网<%s>' % send_email)

    # 主题
    msg['Subject'] = str(Header('CRM系统官网帐号激活邮件', 'utf-8'))

    try:
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(email_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)

        # 登录发送邮箱
        server.login(send_email, passworld)

        # 调用方法  第一个参数是发件人邮箱 第二个参数是接收人的邮箱 第三个是内容
        # server.sendmail(send_email,msg_to.split(',') , msg.as_string())
        server.sendmail(send_email, to_addr, msg.as_string())

        # 关闭发送
        server.close()
        return JsonResponse({'code': 200, 'msg': '注册成功，请前往邮箱激活帐号'})
    except smtplib.SMTPException as e:
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '注册失败，请重新注册'})


# -----------------发送邮件-------end------------------------

# 激活邮件
@require_GET
def active_accounts(request):
    try:
        # 用户名
        username = request.GET.get('username')
        # 激活码
        code = request.GET.get('code')
        # 过期时间
        ts = request.GET.get('timestamp')

        # 根据用户名和激活码查询是否有该帐号
        user = User.objects.get(username=username, code=code, timestamp=ts)

        # 根据过期时间判断帐号是否有效
        now_ts = int(str(datetime.now().timestamp()).split('.')[0])
        if now_ts > int(ts):
            # 链接失效，返回提示信息，删除数据库信息
            user.delete()
            return HttpResponse(
                '<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://127.0.0.1:8000/system/login_register/">上海尚学堂CRM系统</a></h1>')

        # 没有过期，激活帐号，清除激活码，改变状态
        user.code = ''  # 清除激活码
        user.status = 1  # 有效帐号
        user.save()

        # 返回提示信息
        return HttpResponse(
            '<h1>帐号激活成功，请前往系统登录&nbsp;&nbsp;<a href="http://127.0.0.1:8000/system/login_register/">上海尚学堂CRM系统</a></h1>')
    except Exception as e:
        if isinstance(e, User.DoesNotExist):
            return HttpResponse(
                '<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://127.0.0.1:8000/system/login_register/">上海尚学堂CRM系统</a></h1>')
        return HttpResponse('<h1>不好意思，网络出现了波动，激活失败，请重新尝试</h1>')


# 登录
def login_user(request):
    try:
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 使用md5加密
        passwordmd5 = md5(password.encode(encoding='utf-8')).hexdigest()
        # 查询是否存在用户
        user = User.objects.get(username=username, password=passwordmd5)
        # 如果用户存在,储存session信息
        request.session['username_session'] = username
        # 判断是否选择了免登陆,选择设置session的时间
        if 'true' == remember:
            # 设置session失效时间,5天后失效
            request.session.set_expiry(5)
        else:
            # 设置session失效时间,关闭浏览器失效
            request.session.set_expiry(0)

        # 如果用户存在，前台js存储cookie
        # 存储格式：key -> login_cookie, value -> username&password
        context = {'code': 200, 'msg': '欢迎回来'}
        # # 由于功能改造，代码重构
        if 'true' == remember:
            context['login_username_cookie'] = base64.b64encode(username.encode(encoding='utf-8')).decode(
                encoding='utf-8')
            context['login_password_cookie'] = base64.b64encode(password.encode(encoding='utf-8')).decode(
                encoding='utf-8')
        # 存在用户,返回json数据
        return JsonResponse(context)

    except User.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})


# 跳转首页
def index(request):
    # 判断session中是否有用户信息
    username = request.session.get('username_session')
    # 判断浏览器中是否有cookie信息


    if username:
        return render(request, 'system/index.html')

    # 如果不存在，重定向登录页面
    return redirect('system:login_register')


# 跳转忘记密码页面
def forget_password(request):
    return render(request, 'system/forget_password.html')



#验证邮箱跟用户名是否存在
@require_POST
def forget_username(request):
        try:
            # 接收参数,
            username = request.POST.get('username')
            # 查询是否有该用户
            user1 = User.objects.get(username=username)
            if user1:
                # 有用户返回页面json
                return JsonResponse({'code': 200, 'msg': '已查到'})
        except User.DoesNotExist as e:
            # 异常信息说明用户不存在
            return JsonResponse({'code': 400, 'msg': '用户名不存在'})

#验证邮箱是否存在
@require_POST
def forget_email(request):
        try:

            # 接收参数
            email = request.POST.get('email')
            # 查询是否有该用户
            user2 = User.objects.get(email=email)
            if user2:
                # 有用户返回页面json
                return JsonResponse({'code': 200, 'msg': '已查到'})
        except User.DoesNotExist as e:
            # 异常信息说明用户不存在
            return JsonResponse({'code': 400, 'msg': '邮箱不存在'})

@require_POST
def send_email2(request):
    # 发件人邮箱
    send_email = 'm15171636873@163.com'
    # 授权码
    passworld = 'ly1207'

    # 邮件发送的服务器地址
    email_server = 'smtp.163.com'
    # 收件人邮箱
    to_addr = request.POST.get('email')
    # 用户名
    username = request.POST.get('username')
    html = """
        <html>
            <body>
                <div>
                Email 地址验证<br>
                这封信是由 上海尚学堂 发送的。<br>
                您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了密码修改，或用户修改 Email 使用了这个邮箱地址。<br>
                如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                ----------------------------------------------------------------------<br>
                 密码修改说明<br>
                ----------------------------------------------------------------------<br>
                如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                您只需点击下面的链接激活帐号即可：<br>
                <a href="http://127.0.0.1:8000/system/system_updedate_password/">http://www.crm.com/system_updedate_password/</a><br/>
                感谢您的访问，祝您生活愉快！<br>
                此致<br>
                 上海尚学堂 管理团队.
                </div>
            </body>
        </html>"""
    msg = MIMEText(html, "html", "utf-8")
    '''
        构建邮件内容对象
            第一个参数是邮件内容
            第二个参数是MIME，必须是plain即text/plain否则中文不显示
            第三个参数是编码
    '''

    # 标准邮件需要三个头部信息：From To 和 Subject
    # 设置发件人和收件人的信息
    # 比如：尚学堂 <java_mail01@163.com>
    # 发件人
    msg['From'] = format_addr('CRM系统官网<%s>' % send_email)

    # 主题
    msg['Subject'] = str(Header('CRM系统官网帐号激活邮件', 'utf-8'))

    try:
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(email_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)

        # 登录发送邮箱
        server.login(send_email, passworld)

        # 调用方法  第一个参数是发件人邮箱 第二个参数是接收人的邮箱 第三个是内容
        # server.sendmail(send_email,msg_to.split(',') , msg.as_string())
        server.sendmail(send_email, to_addr, msg.as_string())

        # 关闭发送
        server.close()
        return JsonResponse({'code': 200, 'msg': '提交，请前往邮箱修改密码'})
    except smtplib.SMTPException as e:
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '提交失败,请重新填写'})

#跳转修改密码页面

def system_updedate_password(request):
    return render(request, 'system/update_password.html')

# 修改密码
@require_POST
def system_update_btn(request):
    try:
        # 接收参数
        old_password = request.POST.get('pwd1')
        new_password = request.POST.get('pwd2')

        # 使用md5加密
        old_password_md5 = md5(old_password.encode(encoding='utf-8')).hexdigest()

        # 查询用户密码是否正确
        user = User.objects.get(password=old_password_md5)

        # 使用md5加密
        new_password_md5 = md5(new_password.encode(encoding='utf-8')).hexdigest()

        # 修改密码
        user.password = new_password_md5
        user.save()

        # 修改密码要重新登录，所以要安全退出
        # 安全退出系统要清除session，所以这里不写

        # 返回页面信息
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    except User.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': '原密码输入错误'})




# 修改密码
@require_POST
def update_password(request):
    try:
        # 接收参数
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # 使用md5加密
        old_password_md5 = md5(old_password.encode(encoding='utf-8')).hexdigest()

        # 查询用户密码是否正确
        user = User.objects.get(username=username, password=old_password_md5)

        # 使用md5加密
        new_password_md5 = md5(new_password.encode(encoding='utf-8')).hexdigest()

        # 修改密码
        user.password = new_password_md5
        user.save()

        # 修改密码要重新登录，所以要安全退出
        # 安全退出系统要清除session，所以这里不写

        # 返回页面信息
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    except User.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': '原密码输入错误'})
