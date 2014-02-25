__author__ = 'wei'
# -*- coding: utf-8 -*-
#增加了IOS的离线消息推送,IOS不支持IGtNotyPopLoadTemplate模板
#更新时间为2013年12月02日 VERSION: 3.0.0.0
#

from igt_push import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *

import hashlib
import urllib, urllib2, json


APPKEY = "请输入您的appkey"
APPID = "请输入您的appid"
MASTERSECRET = "请输入您的MASTERSECRET"
CID = "请输入您的CID"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

def pushMessageToSingle():


    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 2
    template.transmissionContent = "这是一条toSingle测试消息"
    template.title = "igetui"
    template.text = "click to download"
    template.logo = "icon.png"
    template.logoURL = "http://www.photophoto.cn/m23/086/010/0860100017.jpg"
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    #iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    #template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
    template.setPushInfo("open",4,"message","","","","","");
    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template

    target = Target()
    target.appId = APPID
    target.clientId = CID

    ret = push.pushMessageToSingle(message, target)
    print ret
    return ret


def pushMessageToList():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 2
    template.transmissionContent = "这是一条toList测试消息"
    template.title = "igetui"
    template.text = "click to download"
    template.logo = "icon.png"
    template.logoURL = "http://www.photophoto.cn/m23/086/010/0860100017.jpg"
    template.url = "http://www.baidu.com"
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    #iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    #template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
    template.setPushInfo("open",2,"message","test1.wav","","","","");
    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12

    target1 = Target()
    target1.appId = APPID
    target1.clientId = CID

    target2 = Target()
    target2.appId = APPID
    target2.clientId = CID

    targets = [target1, target2]
    contentId = push.getContentId(message)
    ret = push.pushMessageToList(contentId, targets)
    print ret
    return ret


def pushMessageToApp():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    template = TransmissionTemplate()
    template.transmissionType = 2
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '这是一条toApp测试消息'
    #iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    #template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
    template.setPushInfo("open",1,"message","test1.wav","","","","");	
    message = IGtAppMessage()
    message.data = template
    message.isOffline = True
    #离线的单位时间为毫秒，例，两小时离线时间为 1000*3600*2，以此类推
    message.offlineExpireTime = 1000 * 3600 * 12
    message.appIdList.extend([APPID])
    #message.phoneTypeList.extend(["ANDROID", "IOS"])
    #message.provinceList.extend(["浙江", "上海"])

    ret = push.pushMessageToApp(message)
    print ret
    return ret

def getPushResult(url,appKey,masterSecret,taskId):
    params = {}
    params["action"] = "getPushMsgResult"
    params["appkey"] = appKey
    params["taskId"] = taskId
    sign = createSign(params,masterSecret)
    params["sign"] = sign
    rep = httpPost(url,params)
    print rep
    return rep

def createSign(params,masterSecret):
    sign = masterSecret
    for (k,v) in params.items():
        sign = sign+k+v
    return hashlib.md5(sign).hexdigest()
def httpPost(url, params):
    data_json = json.dumps(params)
    req = urllib2.Request(url, data_json)
    res_stream = urllib2.urlopen(req, timeout = 60)
    page_str = res_stream.read()
    page_dict = eval(page_str)
    return page_dict

result = pushMessageToSingle()
getPushResult(HOST, APPKEY, MASTERSECRET, result['taskId'])

result_list = pushMessageToList()

getPushResult("http://sdk.open.api.igexin.com/api.htm", APPKEY, MASTERSECRET, result_list['contentId'])

result_app = pushMessageToApp()

getPushResult("http://sdk.open.api.igexin.com/api.htm", APPKEY, MASTERSECRET, result_app['contentId'])









