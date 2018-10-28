from django.db import models
from datetime import datetime


# 用户模型
class User(models.Model):
    # 用户名
    username = models.CharField(max_length=20, db_column='user_name')
    # 密码
    password = models.CharField(max_length=100)
    # 真实姓名
    truename = models.CharField(max_length=20, null=True, db_column='true_name')
    # 邮箱
    email = models.CharField(max_length=30)
    # 手机号
    phone = models.CharField(max_length=20, null=True)
    #是否有效
    is_valid = models.IntegerField(max_length=4, default=1)
    #创建日期
    create_date = models.DateTimeField(default=datetime.now())
    #修改时间
    update_date = models.DateTimeField(null=True)
    #激活码
    code = models.CharField(max_length=255, null=True)
    #状态
    status = models.BooleanField(max_length=1, default=0)
    #时间戳
    timestamp = models.CharField(max_length=255, null=True)

    # 元信息
    class Meta(object):
        db_table = 't_user'
