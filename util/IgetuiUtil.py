#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk.igt_push import *
from sdk.igetui.template.igt_base_template import *
from sdk.igetui.template.igt_transmission_template import *
from sdk.igetui.template.igt_link_template import *
from sdk.igetui.template.igt_notification_template import *
from sdk.igetui.igt_message import *
from sdk.igetui.igt_target import *
from sdk.igetui.template import *

import settings

igetui_config = settings.igetui_config

APPKEY = igetui_config['APPKEY']
APPID = igetui_config['APPID']
MASTERSECRET = igetui_config['MASTERSECRET']
CID = igetui_config['CID']
HOST = igetui_config['HOST']

def pushMessageToSingle(
        template = NotificationTemplate(),
        isOffline = True,
        offlineExpireTime = 1000 * 3600 * 12,
        appId = igetui_config['APPID'],
        appKey = igetui_config['APPKEY'],
        host = igetui_config['HOST'],
        masterSecret = igetui_config['MASTERSECRET'],
        cid = igetui_config['CID'],
        provinceList = [],
        phoneTypeList = []):
    '''
    ##对单个用户推送
    *   isOffline: 是否离线,2为离线推送，默认为2，
    *   offlineExpireTime: 离线时间，单位为毫秒，例，两小时离线时间为 1000*3600*2，以此类推
    *   appId: 应用appid
    *   appKey: 应用appKey
    *   host: push server url, 在setting中定义
    *   masterSecret: push平台每个应用省城的masterSecret序列号
    *   cid: clientId
    *   provinceList: 区域推送列表
    *   phoneTypeList: 手机平台类型推送列表
    '''
    template.appId = appId
    template.appKey = appKey

    message = IGtSingleMessage()
    message.isOffline = isOffline
    message.offlineExpireTime = offlineExpireTime
    message.data = template
    message.phoneTypeList.extend(phoneTypeList)
    message.provinceList.extend(provinceList)

    target = Target()
    target.appId = appId
    target.clientId = cid

    push = IGeTui(host, appKey, masterSecret)
    ret = push.pushMessageToSingle(message, target)
    print ret    

def pushMessageToList(
        template = NotificationTemplate(),
        isOffline = True,
        offlineExpireTime = 1000 * 3600 * 12,
        appId = igetui_config['APPID'],
        appKey = igetui_config['APPKEY'],
        host = igetui_config['HOST'],
        masterSecret = igetui_config['MASTERSECRET'],
        cidList = [igetui_config['CID']],
        provinceList = [],
        phoneTypeList = []):
    '''
    ##通过ClientID列表群推送
    *   isOffline: 是否离线,2为离线推送，默认为2，
    *   offlineExpireTime: 离线时间，单位为毫秒，例，两小时离线时间为 1000*3600*2，以此类推
    *   appId: 应用appid
    *   appKey: 应用appKey
    *   host: push server url, 在setting中定义
    *   masterSecret: push平台每个应用省城的masterSecret序列号
    *   cidList: clientId List
    *   provinceList: 区域推送列表
    *   phoneTypeList: 手机平台类型推送列表
    '''
    template.appId = appId
    template.appKey = appKey

    message = IGtListMessage()
    message.isOffline = isOffline
    message.offlineExpireTime = offlineExpireTime
    message.data = template
    message.phoneTypeList.extend(phoneTypeList)
    message.provinceList.extend(provinceList)

    targets = []
    for cid in cidList:
        target = Target()
        target.appId = appId
        target.clientId = cid
        targets.append(target)

    push = IGeTui(host, appKey, masterSecret)
    contentId = push.getContentId(message)
    ret = push.pushMessageToList(contentId, targets)
    print ret

def pushMessageToApp(
        template = NotificationTemplate(),
        isOffline = True,
        offlineExpireTime = 1000 * 3600 * 12,
        appId = igetui_config['APPID'],
        appKey = igetui_config['APPKEY'],
        host = igetui_config['HOST'],
        masterSecret = igetui_config['MASTERSECRET'],
        provinceList = [],
        phoneTypeList = []):
    '''
    ##通过应用(AppID 列表)群推,给所有符合条件的客户端用户推送
    *   isOffline: 是否离线,2为离线推送，默认为2，
    *   offlineExpireTime: 离线时间，单位为毫秒，例，两小时离线时间为 1000*3600*2，以此类推
    *   appId: 应用appid
    *   appKey: 应用appKey
    *   host: push server url, 在setting中定义
    *   masterSecret: push平台每个应用省城的masterSecret序列号
    *   provinceList: 区域推送列表
    *   phoneTypeList: 手机平台类型推送列表
    '''
    template.appId = appId
    template.appKey = appKey

    message = IGtAppMessage()
    message.isOffline = isOffline
    message.offlineExpireTime = offlineExpireTime
    message.data = template
    message.appIdList.extend([appId])
    message.phoneTypeList.extend(phoneTypeList)
    message.provinceList.extend(provinceList)

    push = IGeTui(host, appKey, masterSecret)
    ret = push.pushMessageToApp(message)
    print ret

def generateTrasmissionTemplate(
        transmissionType = 2,
        transmissionContent = ""):
    '''
    ##生成透传模板
    *   transmissionType: 收到消息是否立即启动应用, 1 为立即启动,2 则广播等待客户端自启动
    *   transmissionContent: 透传内容,不支持转义字符
    '''
    template = TransmissionTemplate()
    template.transmissionType = transmissionType
    template.transmissionContent = transmissionContent
    return template

def generateNotificationTemplate(
        transmissionType = 2,
        transmissionContent = "",
        title = "",
        text = "",
        logo = "",
        isRing = True,
        isVibrate = True,
        isClearable = True):
    '''
    ##生成通知模板
    *   transmissionType: 收到消息是否立即启动应用, 1 为立即启动,2 则广播等待客户端自启动
    *   transmissionContent: 透传内容,不支持转义字符
    *   title: 通知栏标题
    *   text: 通知栏内容
    *   logo: 通知的图标名称,包含后缀名(需要在客户端开发时嵌入),如“push.png”
    *   isRing: 收到通知是否响铃: true 响铃,false 不响铃。默认响铃。
    *   isVibrate: 收到通知是否振动: true 振动,false 不振动。默认振动。
    *   isClearable: 通知是否可清除: true 可清除,false 不可清除。默认可清除。
    '''
    template = NotificationTemplate()
    template.transmissionType = transmissionType
    template.transmissionContent = transmissionContent
    template.title = title
    template.text = text
    template.logo = logo
    template.isRing = isRing
    template.isVibrate = isVibrate
    template.isClearable = isClearable
    return template

def generateLinkTemplate(
        url = "",
        title = "",
        text = "",
        logo = "",
        isRing = True,
        isVibrate = True,
        isClearable = True):
    '''
    ##生成链接模板
    *   url: 点击通知后打开的网页地址
    *   title: 通知栏标题
    *   text: 通知栏内容
    *   logo: 通知的图标名称,包含后缀名(需要在客户端开发时嵌入),如“push.png”
    *   isRing: 收到通知是否响铃: true 响铃,false 不响铃。默认响铃。
    *   isVibrate: 收到通知是否振动: true 振动,false 不振动。默认振动。
    *   isClearable: 通知是否可清除: true 可清除,false 不可清除。默认可清除。
    '''
    template = LinkTemplate()
    template.url = url
    template.title = title
    template.text = text
    template.logo = logo
    template.isRing = isRing
    template.isVibrate = isVibrate
    template.isClearable = isClearable
    return template















