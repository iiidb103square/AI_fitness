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

from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, URIAction
import os

from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, URIAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)



def Pose(event):  #圖片轉盤
    print("### module.sendCarousel.Pose")
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://mmbiz.qpic.cn/mmbiz_gif/BIatWXEC82a8OZkXr3tYwIpzNJulySPHZuZftKf5B7w3wcGrjerpicMI5BSCPXGsPwmE6qzpgFfr1jGkxkoqpPA/640?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1',
                        action=URITemplateAction(
                            label='深蹲20下',
                            uri='line://app/1653356616-5Jkb6kLV'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://s3-ap-southeast-1.amazonaws.com/img.khoobsurati.com/wp-content/uploads/2015/05/img-Push-Ups-2018-07.gif',
                        action=URITemplateAction(
                            label='伏地挺身20下',
                            uri='line://app/1653356616-5Jkb6kLV'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://cdn.shopify.com/s/files/1/1501/0558/files/SitUp.gif?v=1514735483',
                        action=URITemplateAction(
                            label='仰臥起坐20下',
                            uri='line://app/1653356616-5Jkb6kLV'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://us.123rf.com/450wm/logo3in1/logo3in11510/logo3in1151000001/46716051-woman-making-perfect-body-with-the-plank-exercis.jpg?ver=6',
                        action=URITemplateAction(
                            label='棒棒式40秒',
                            uri='line://app/1653356616-5Jkb6kLV'
                        )
                    )

                ]
            )
        )        
        
        #return HttpResponse()
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
