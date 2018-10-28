"""py_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'system'
urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('verify_username/', views.verify_username, name='verify_username'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('send_email/', views.send_email, name='send_email'),
    path('active_accounts/', views.active_accounts, name='active_accounts'),
    path('login_user/', views.login_user, name='login_user'),
    path('index/', views.index, name='index'),
    path('update_password/', views.update_password, name='update_password'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forget_username/', views.forget_username, name='forget_username'),
    path('forget_email/', views.forget_email, name='forget_email'),
    path('send_email2/', views.send_email2, name='send_email2'),
    path('system_updedate_password/', views.system_updedate_password, name='system_updedate_password'),
    path('system_update_btn/', views.system_update_btn, name='system_update_btn'),



]
