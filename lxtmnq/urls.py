#/usr/bin/env python3
# -*- coding:utf-8 -*-

"""lxtmnq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from sign import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reset-password/index$', views.index_of_reset_password),#交易密码重置
    url(r'^open-acct/index$', views.index_of_open_acct),#开户
    url(r'^change-bank-card/index$', views.index_of_change_bank_card),#更换银行卡
    url(r'^stock-customer/index$', views.index_of_stock_customer),#已迁移未开通
    url(r'^unbind/index$', views.index_of_unbind),#解绑银行卡

    url(r'^payment-confirm/index$', views.index_of_payment_confirm),#缴费申请
    url(r'^business-authorize-confirm/index$', views.index_of_business_authorize_confirm),#投资免密y y
    url(r'^bespeak-investment-freeze-confirm/index$', views.index_of_bespeak_investment_freeze_confirm),#预约投资y y
    url(r'^investment-freeze-confirm/index$', views.index_of_investment_freeze_confirm),#投资y
    url(r'^withdrawals-confirm/index$', views.index_of_withdrawals_confirm),#提现y
    url(r'^recharge-confirm/index$', views.index_of_recharge_confirm),#充值
    url(r'^pay-confirm/index$', views.index_of_pay_confirm),#定向支授权
    url(r'^unsubscribe/index$', views.index_of_unsubscribe),#销户
    url(r'^update-action/$', views.update_action),#修改返回pjs的报文
    url(r'^testa/', views.testa),
]
