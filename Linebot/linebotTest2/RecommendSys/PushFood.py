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
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def PushFood(event, Push):
    print("="*100)
    print("="*100)
    print("### PushFood.PushFood")
    print(event)
    Push0a = Push[0][0]
    Push1a = Push[1][0]
    Push2a = Push[2][0]    
    
    print("### PushFood.PushFood.食物順序重整_start")
    i = 0
    Push0b = ("食用量："       + str(Push[i][1]) + "   " + 
             "熱量(大卡)："    + str(Push[i][2]) + "\n" +
             "脂肪(克)："      + str(Push[i][4]) + "  " +
             "蛋白質(克)："    + str(Push[i][5]) + "\n" + 
             "碳水化合物(克)："+ str(Push[i][3])
            )
    i = 1
    Push1b = ("食用量："       + str(Push[i][1]) + "   " +  
             "熱量(大卡)："    + str(Push[i][2]) + "\n" +
             "脂肪(克)："      + str(Push[i][4]) + "  " +
             "蛋白質(克)："    + str(Push[i][5]) + "\n" + 
             "碳水化合物(克)："+ str(Push[i][3])
            )
    i = 2
    Push2b = ("食用量："       + str(Push[i][1]) + "   " +  
             "熱量(大卡)："    + str(Push[i][2]) + "\n" +
             "脂肪(克)："      + str(Push[i][4]) + "  " +
             "蛋白質(克)："    + str(Push[i][5]) + "\n" + 
             "碳水化合物(克)："+ str(Push[i][3])
            )
    print(Push0a + Push0b + "\n" +
          Push1a + Push1b + "\n" +
          Push2a + Push2b + "\n" )
    print("### PushFood.PushFood.食物順序重整_end") 
    try:
        print("### PushFood.PushFood.try_start")
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
               columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.team17.com/wp-content/uploads/2018/08/Nintendo-Switch-exclusive-chef.gif',# 鴨嘴獸大師
                        title= Push2a,
                        text= Push2b,
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='賣披薩'
                            ),
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.team17.com/wp-content/uploads/2018/08/Racoon.gif',# 浣熊大師
                        title= Push0a,
                        text= Push0b,
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='賣披薩'
                            ),
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息一',
                                data='action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.team17.com/wp-content/uploads/2018/08/Unicorn.gif', # 查理大師
                        title=Push1a,
                        text=Push1b,
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息二',
                                text='賣飲料'
                            ),
                            URITemplateAction(
                                label='連結台大網頁',
                                uri='http://www.ntu.edu.tw'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息二',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

