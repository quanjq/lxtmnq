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



dict_t036={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "reqSn":'',
           "retcode":"00000",
           "errCode":"0000",
           "errMsg" :"处理成功",
           "settleDay":"",
           "retMsg":"充值确认交易成功."}
def index_of_recharge_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t036_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t036_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0360000001'
    ret_text={}
    for key,valu in dict_t036.items():
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['reqSn']=dec_ext['reqSn']
    ret_text['settleDay']=time.strftime('%y%m%d',time.localtime(time.time()))
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg

dict_t003={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "frzNo":"",
           "reqSn":'',
           "accBal":"",
           "freezeAmt":"",
           "retcode":"00000",
           "retMsg":"提现确认交易成功."}
def index_of_withdrawals_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t003_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t003_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0030000001'
    ret_text={}
    for key,valu in dict_t003.items():
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['reqSn']=dec_ext['reqSn']
    ret_text['frzNo']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg


dict_t007={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "frzNo":"",
           "refNo":"",
           "retcode":"00000",
           "retMsg":"冻结成功."}
def index_of_investment_freeze_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t007_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t007_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0070000001'
    ret_text={}
    for key,valu in dict_t007.items():
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['refNo']=dec_ext['refNo']
    ret_text['frzNo']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg

dict_t006={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "frzNo":"",
           "frzType":"",
           "refNo":"",
           "retcode":"00000",
           "retMsg":"缴费确认交易成功."}
def index_of_bespeak_investment_freeze_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t006_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t006_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0060000001'
    ret_text={}
    for key,valu in dict_t006.items():  #复制dict_t037的值而不改变dict_t037的值
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['refNo']=dec_ext['refNo']
    ret_text['frzType']=dec_ext['frzType']
    ret_text['frzNo']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg

dict_t013={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "refNo":"",
           "retcode":"00000",
           "retMsg":"缴费确认交易成功."}
def index_of_business_authorize_confirm(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t013_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t013_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0130000001'
    ret_text={}
    for key,valu in dict_t013.items():  #复制dict_t037的值而不改变dict_t037的值
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['refNo']=dec_ext['refNo']
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg

dict_t037={"orgCode":"105584099990002",
           "custId":"",
           "traceNo":"",
           "authNo":"",
           "refNo":"",
           "retcode":"00000",
           "retMsg":"缴费确认交易成功."}
def index_of_payment_confirm(request):
    ###t037逾期缴费，先后台发送建行后才前端post请求
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t037_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def index_of_pay_confirm(request):
    ###t037逾期缴费，先后台发送建行后才前端post请求
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            recevieUrl,res_data,retmsg=t037_msg(dec_ext)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t037_msg(dec_ext):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T0370000001'
    ret_text={}
    for key,valu in dict_t037.items():  #复制dict_t037的值而不改变dict_t037的值
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['traceNo']=traceNo
    ret_text['authNo']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'60000001'
    ret_text['refNo']=dec_ext['refNo']
    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg



port=8220 #前置机的端口号,这是公用的，需要提取出来
dict_t039={"orgCode":"105584099990002",
           "custId":"",
           "custNm":"",
           "telNo":"13580420001",
           "bankNm":"308",
           "acctNo":"99990000000001",
           "retCode":"00000",
           "retMsg":"测试成功",
           "traceNo":"181220141937TL022068539",
           "oprFlag":""}
dict_oprFlag_t039={'reset_password':'0007',#重置交易密码
                   'open_acct':'0001',#新用户开户
                   'change_bank_card':'0002',#更换银行卡
                   'stock_customer':'0003',#已迁移未开通
                   'unbind':'0005',#解绑卡信息
                   'unsubscribe':'0004',#销户
                   }
def index_of_unsubscribe(request):###这个不确定S
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='unbind'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def index_of_unbind(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='unbind'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def index_of_reset_password(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='reset_password'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def index_of_stock_customer(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='stock_customer'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def index_of_open_acct(request):#change_bank_card
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='open_acct'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
            #return HttpResponseRedirect(recevieUrl)  #只能重定向url，只能get请求，不符合
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)
def index_of_change_bank_card(request):
    try:
        if request.method =='POST':
            encryptMsg=request.POST.get("encryptMsg","")
            if encryptMsg==None:
                return  HttpResponse(u'参数有误')
            #1、解密提取报文信息
            dec_ext=json.loads(enc.decrypt(encryptMsg)) #解密提取报文信息json.loads()函数是将json格式数据转换为字典
            log_debug.logger.info('接收到pjs的请求：%s' %dec_ext)
            #2、提取custId、custNm、recevieUrl，新生成traceNo并组装返回给pjs的post报文
            oprflag='change_bank_card'
            recevieUrl,res_data,retmsg=t039_msg(dec_ext,oprflag)
            log_debug.logger.info('回调pjs的报文：%s' %retmsg)
            res_data=res_data.decode('utf-8')
            #3、根据recevieUrl，post相应的 pjs环境# 这里实现是先render并把encryptMsg的数据带过去，然后通过form表单将数据post请求回到pjs页面
            return render(request,'post-to-pjs.html',{"recevieUrl":recevieUrl,'encryptMsg':res_data,'encryptedText':dec_ext,'retmsg':retmsg})
        else:
            return  HttpResponse(u"通讯失败")
    except Exception as e:
        log_error.logger.error(e)

def t039_msg(dec_ext,oprflag):
    oprFlag=dict_oprFlag_t039[oprflag]
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T039000'+oprFlag
    ret_text={}
    for key,valu in dict_t039.items():  #复制dict_t039的值而不改变dict_t039的值
        ret_text[key]=valu
    ret_text['custId']=dec_ext['custId']
    ret_text['custNm']=dec_ext['custNm']
    ret_text['traceNo']=traceNo
    ret_text['oprFlag'] =oprFlag
    if oprFlag=="0001"  :
        ret_text['receiveChannelType']="2"
    elif oprFlag=="0002":
        ret_text['receiveChannelType']="2"
    elif oprFlag=="0003":
        ret_text['receiveChannelType']="2"
    elif oprFlag=="0005":
        ret_text['receiveChannelType']="2"

    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg


def pack_msg(dec_ext,dict):
    traceNo=time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))+'T9990000001'
    frzNo=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'01'
    settleDay=time.strftime('%y%m%d',time.localtime(time.time()))

    ret_text={}
    for key,valu in dict.items():  #复制dict_t039的值而不改变dict_t039的值
        ret_text[key]=valu
    for ke,v in ret_text.items():
        if v[0]==0:   #0取dict本身的值，1取得dec_ext的值，2取公共的
            ret_text[ke]=v[1]
        elif v[0]==1:
            ret_text[ke]=dec_ext[ke]
        else:
            if ke =='traceNo':
                ret_text[ke]=traceNo
            elif ke =='frzNo':
                 ret_text[ke]=frzNo
            elif ke =='settleDay':
                ret_text[ke]=settleDay

    recevieUrl=str(dec_ext['recevieUrl'])
    retmsg=json.dumps(ret_text) #建行/联信通返回的数据
    res_data=enc.encrypt(json.dumps(ret_text).encode('utf-8')) #json.dumps()函数是将一个Python数据类型列表进行json格式的编码
    return  recevieUrl,res_data,retmsg





