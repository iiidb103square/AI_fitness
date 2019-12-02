#!/usr/bin/env python
#coding=utf-8

# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, URIAction,  CameraAction, CameraRollAction,  PostbackAction, PostbackEvent

import os, datetime
from PAL import Path

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def UserData(event):
    try:
        # 取得時間(至十分)
        ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
        time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
        print("### sendText." + time)

        # 存擋路徑
        path = Path() + event.source.user_id + "_" + time

        # 創建file，供module.bodyType使用
        f  = open(path,"w")
        f.write('img') #####內文為'img'        
        f.close()

        print("### QuickReplyButton.UserData_Start\n")
        message = TextSendMessage(
            text='請選擇更新「體態影像」或「身體數值」',
            quick_reply=QuickReply(
                items=[
                   QuickReplyButton( # 打開相機
                        action=CameraAction(label="一定要正面照喔~")
                   ),
                   QuickReplyButton(
                        action=MessageAction(label="更新身體數值",
                                text = "讓我記錄這美好的body吧~")
                   )
                ]
            )
        )

        print("### QuickReplyButton.UserData.messages: ", message)        
        print("### QuickReplyButton.UserData_End\n")

        line_bot_api.reply_message(event.reply_token,message)
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def QR_ExtraFood(event):
    try:
        print("### QuickReplyButton.QR_ExtraFood_Start\n")
        message = TextSendMessage(
            text='請選擇「模糊搜尋」或「精準搜尋」:',
            quick_reply=QuickReply(
                items=[
                   QuickReplyButton(
                         action=PostbackAction(label="模糊搜尋", data="fuzzySearch")
                   ),
                   QuickReplyButton(
                         action=PostbackAction(label="精準搜尋", data="preciseSearch")
                   )
                ]
            )
        )
        print("### QuickReplyButton.QR_ExtraFood.message: ", message)
        print("### QuickReplyButton.QR_ExtraFood_End\n")
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
