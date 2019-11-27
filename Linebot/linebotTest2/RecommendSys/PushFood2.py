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

def PushFood2(event, Push):
    print("="*100)
    print("="*100)
    print("### PushFood2.PushFood")
    print(event)
    Push0a = Push[0][0]
    Push1a = Push[1][0]
    Push2a = Push[2][0]    
    
    print("### PushFood.PushFood2.食物順序重整_start")
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
    print("### PushFood.PushFood2.食物順序重整_end") 
    try:
        print("### PushFood.PushFood2.try_start")
        
        message = TemplateSendMessage(
                alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.team17.com/wp-content/uploads/2018/08/Unicorn.gif',  #顯示的圖片
                title='查理大師的建議',  #主標題
                text='抖雞(請選擇)：',  #副標題
                actions=[
                    MessageTemplateAction(  #顯示文字計息
                        label= Push0a,
                        text= ('我想吃查理大師的 \n「 '+ Push0a + '」')

                    ),
                    MessageTemplateAction( 
                        label= Push1a,
                        text= ('我想吃查理大師的 \n「 '+ Push1a + '」')
                    ),
                    MessageTemplateAction( 
                        label= Push2a,
                        text= ('我想吃查理大師的 \n「 '+ Push2a + '」')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

