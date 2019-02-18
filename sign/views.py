#/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: quanjq
@file: views.py
@time: 2019/1/2 10:00
"""

import sys
import os
dir_sign=os.path.split(os.path.realpath(__file__))[0] #将当前的目录sign加入sys的path路径，方便 python执行时能够找到自定义的库
sys.path.append(dir_sign)

# Create your views here.
from lib.EncryptUtil import  EncryptUtil
pub_key_path=dir_sign+'/lib/pub.key'
pri_key_path=dir_sign+'/lib/pri.key'
enc=EncryptUtil(pub_key_path,pri_key_path)

from django.shortcuts import render
import json
from django.http import HttpResponse
from lib.Logger import Logger
import time
######1、接收到post请求，解密
########2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
########3、根据recevieUrl，post相应的 pjs环境
########4、组装xml报文，发送给pjs前置机 这个暂时不开发

log_debug = Logger('all.log',level='debug')
log_error=Logger('error.log', level='error')



recharge_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "reqSn":[1],
		   "errCode":[0,'0000'],
		   "errMsg":[0,'success'],
		   "settleDay":[2],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_recharge_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=recharge_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

withdrawals_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "reqSn":[1],
		   "accBal":[0,''],
		   "frzNo":[2],
		   "freezeAmt":[0,''],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_withdrawals_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=withdrawals_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)


investment_freeze_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
            "frzNo":[2],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_investment_freeze_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=investment_freeze_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

bespeak_investment_freeze_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
            "frzNo":[2],
            "frzType":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_bespeak_investment_freeze_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=bespeak_investment_freeze_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

business_authorize_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}

def index_of_business_authorize_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=business_authorize_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

payment_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "authNo":[1],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_payment_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=payment_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)


unsubscribe_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0004']}
def index_of_unsubscribe(request):###这个不确定S
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=unsubscribe_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
unbind_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0005']}
def index_of_unbind(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=unbind_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
reset_password_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0007']}
def index_of_reset_password(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=reset_password_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            # post_to_pjs(recevieUrl,res_data)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

import requests
def post_to_pjs(recevieUrl,res_data):
    # url='http://127.0.0.1:8000/testa/'
    post_data="encryptMsg="+res_data
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    requests.post(recevieUrl,data=post_data,headers=headers)


stock_customer_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0003']}
def index_of_stock_customer(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=stock_customer_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
open_acct_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0001']}
def index_of_open_acct(request):#change_bank_card
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=open_acct_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
change_bank_card_dict={"orgCode":[1],
           "custId":[1],
           "custNm":[1],
           "telNo":[0,"13580420001"],
           "bankNm":[0,"308"],
           "acctNo":[0,"99990000000001"],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."],
           "traceNo":[2],
           "oprFlag":[0,'0002']}
def index_of_change_bank_card(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=change_bank_card_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

pay_confirm_dict={"orgCode":[1],
           "custId":[1],
           "traceNo":[2],
           "authNo":[2],
           "refNo":[1],
           "retcode":[0,"00000"],
           "retMsg":[0,"testsuccess."]}
def index_of_pay_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            dict_tex=pay_confirm_dict
            recevieUrl,res_data,retmsg,dec_ext=proce(encryptMsg,dict_tex)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)


def proce(encryptMsg,dict_text):
     #1、解密提取报文信息
     dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
     log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
     #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
     recevieUrl,res_data,retmsg=pack_msg(dec_ext,dict_text)
     log_debug.logger.info('回调pjs的报文明文：%s' %retmsg)
     res_data=res_data.decode('utf-8')
     log_debug.logger.info('回调pjs的报文密文：%s' %res_data)
     #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
     return  recevieUrl,res_data,retmsg,dec_ext

def pack_msg(dec_ext,dict):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T9990000001'
    frzNo=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    settleDay=time.strftime('%y%m%d',time.localtime(time.time()))
    authNo=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'60000001'

    ret_text={}
    for key,valu in dict.items():  #复制dict_t039的值而不改变dict_t039的值
        ret_text[key]=valu
    for ke,v in ret_text.items():
        if v[0]==0:   #0取dict本身的值，1取得dec_ext的值，2取公共的
            ret_text[ke]=v[1]
        elif v[0]==1:
            ret_text[ke]=dec_ext[ke]
        elif v[0]==2:
            if ke =='traceNo':
                ret_text[ke]=traceNo
            elif ke =='frzNo':
                 ret_text[ke]=frzNo
            elif ke =='authNo' :
                ret_text[ke]=authNo
            elif ke =='settleDay':
                ret_text[ke]=settleDay

    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    #retmsg=ret_text #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg

def update_action(request):
    try:
        if request.method =='POST':
            msg=request.POST.get("msg_from_lxt","")
            dec_ext=request.POST.get("msg_from_pjs","")
            log_debug.logger.info('修改的报文明文：%s' %msg)
            recevieUrl=request.POST.get("msg_recevieUrl","")
            print msg
            print dec_ext
            print recevieUrl
            if msg==None:
                return  HttpResponse(u'参数有误')
            res_data=enc.encrypt(msg.encode('utf-8'))
            res_data=res_data.decode('utf-8')
            log_debug.logger.info('修改的报文密文：%s' %res_data)
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':msg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def testa(request):
    encryptMsg=request.POST.get("encryptMsg","")
    # print encryptMsg
    return render(request,'post-to-pjs.html')