# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-

import urllib.parse
import requests

sms_send_url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"

# 用户名是登录ihuyi.com账号名（例如：cf_demo123）
account = "account"
# 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "password"


def send_sms(text, mobile):
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    response = requests.post(sms_send_url, params='', data=params, headers=headers)

    return response.text


