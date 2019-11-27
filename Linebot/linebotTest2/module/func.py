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
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, URIAction, MessageEvent

import os, datetime
from PAL import Path
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def sendText(event):
    from PAL import Path

    # 取得時間(至十分)
    ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
    time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
    print("### sendText." + time)    

    # 存擋路徑
    path = Path() + event.source.user_id + "_" + time

    try:
        mtext = event.message.text
        print("### func.sendText_start\n")    


    # 回覆基本資料的快速選單
        if mtext == "讓我記錄這美好的body吧~":
            #print("### func.sendText.'賞你傳送捲軸，自己更新啦!_start'\n")
            message = TextSendMessage(text = "賞你傳送捲軸，自己更新啦! \n line://app/1653356616-2QDQMDzj")
            #print("### func.sendText.'賞你傳送捲軸，自己更新啦!_end'\n")	
            line_bot_api.reply_message(event.reply_token,message)
            print("### func.UserData.讓我記錄這美好的body吧~_end\n")

    # 尋找夥伴
        elif mtext == "我不想再當單身狗了(〓￣(∵エ∵)￣〓)":
            message = [  #串列
                TextSendMessage(  #傳送y文字
                    text = "我覺得麵包比較重要啦~~~"
                ),
                StickerSendMessage(  #傳送貼圖
                    package_id='2',  
                    sticker_id='175'
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)

    # 嘴饞紀錄
        elif mtext == "人家想知道吃進了多少熱量嘛~ (￣￢￣)~":
            print("func.sendText.人家想知道吃進了多少熱量嘛~ (￣￢￣)~")
            # 創建file，供func.fuzzySearch使用
            f  = open(path,"w")
            f.write('ExtraFood') #####內文為'ExtraFood'
            f.close() 
            # response
            message =TextSendMessage(text = "吃了什麼?跟我說說~\n(在對話框輸入即可)")
            line_bot_api.reply_message(event.reply_token,message)


    # 錯誤回報 
        elif mtext == "我要告狀！(╬ಠ益ಠ)":
            print("func.sendText.我要告狀！(╬ಠ益ಠ)")           

        
            # 創建file，供func.sendErrorReport使用
            f  = open(path,"w")
            f.write('ErrorReport') #####內文為'我要告御狀'
            f.close()
                        
            # response
            message =TextSendMessage(text = "有什麼冤屈儘管說吧!\n(在對話框輸入即可)")
            line_bot_api.reply_message(event.reply_token,message)

    except:
        print("func.sendText.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



# 傳送錯誤報告
def sendErrorReport(event):    
  
    # 取得時間(至十分)
    ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
    time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
    print("### fun.sendErrorReport." + time)
    # 存擋路徑
    path = Path() + event.source.user_id + "_" + time

    try:
        mtext = event.message.text
        print("### func.sendErrorReport_start\n")
        # 傳送錯誤回報給資料庫
        print("### func.sendErrorReport.傳送錯誤回報給資料庫\n")
        print("傳送的資料：", mtext)





        # 刪除 file ，以避免下次回報錯誤
        os.remove(path)
        print("### func.sendErrorReport.刪除 file\n")

        # reponse
        print("### func.sendErrorReport.告狀內容：\n \n「" ,mtext, "」\n \n嗯...似乎有參考價值_start\n") 
        print("### user_id:"+ event.source.user_id + "回報時間:" + time)
      
        message = TextSendMessage(text = ("告狀內容：\n \n「"+ mtext  +"」\n \n 嗯...似乎有參考價值"))

        print("### func.sendErrorReport.告狀內容：\n \n「", mtext, "\n \n嗯...似乎有參考價值_end\n") 

        line_bot_api.reply_message(event.reply_token,message)

    except:
        print("func.sendText.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage
(text='發生錯誤！'))


def fuzzySearch(event):
    print("func.fuzzySearch_start")

    # 取得時間(至十分)
    ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
    time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
    print("### func.fuzzySearch." + time)
    # 存擋路徑
    path = Path() + event.source.user_id + "_" + time
    # 讀檔路徑
    pathForLoad = Path()
    
    try:
        import pandas as pd
        import numpy as np

        print("### func.fuzzySearch.讀檔路徑:", pathForLoad)   
        df = pd.read_csv(pathForLoad + '../RecommendSys/Food_Mixed2.csv', encoding='utf8') # 讀取資料
        df = df.drop_duplicates(subset='Name', keep='first') # 刪除df['Name']重複值，並僅取第一個
        df = df[['Name', 'Intake_g', 'Cal_kcal', 'Protein_g', 'Fat_g', 'CHO_g']] # 僅取有需要的營養成分
        df = df.reset_index(drop=True) # 重整df_food_g之索引
        
        keyWord = event.message.text  # 搜尋關鍵字    

        
        # 精準搜尋
        print("### func.fuzzySearch.精準搜尋")
        preciseSearch = df[df['Name'] == keyWord] 
        print("### func.fuzzySearch.精準搜尋.preciseSearch: ", preciseSearch)
          
        if  len(preciseSearch) == 1:
                
            print(preciseSearch.iloc[0])
            i = preciseSearch.iloc[0]

            preciseSearch = ("品名："          +str(i[0]) + "\n" +
                              "食用量："        +str(i[1]) + "\n" +
                              "熱量(大卡)："    + str(i[2]) + "\n" +
                              "脂肪(克)："      + str(i[4]) + "\n" +
                              "蛋白質(克)："    + str(i[5]) + "\n" +
                              "碳水化合物(克)："+ str(i[3]) )

            text_ = ("偷吃了:\n \n" + preciseSearch + "\n \n 哼哼! \n 我就直接記錄下來嘍(*￣3￣)╭“") #要印的語句
            print(text_)
                
            os.remove(path)
            print("### func.fuzzySearch.精準搜尋.刪除file\n")        
   
            message = TextSendMessage(text = text_)
            line_bot_api.reply_message(event.reply_token,message) # 送出
   
        else:
 
            print("### func.fuzzySearch.模糊搜尋")
            # 模糊搜尋
            bool_ = df['Name'].str.contains(keyWord)  # 抓出有關鍵字之資料
            food = df[bool_] 
            food  = food.reset_index(drop=True) # 重整df_food_g之索引
            if len(food)>1:
   
                if len(food) > 10:
                    food = food.sample(n=10)              
                    food = food.reset_index(drop=True) # 重整df_food_g之索引


                #將食物名轉換成字串，方便輸出
                foodList=""
                for i in range(len(food['Name'])):
                    foodList = foodList + "\n" + str(food['Name'][i]) 
                 
                text_ = ("相似的食物有:\n "+foodList+"\n \n 是哪一個啊?\n\n(請在對話框輸入\n若以上皆非，請再輸入關鍵字)")
                print(text_)
                message = TextSendMessage(text = text_)
     
            else:
                text_ = '抱歉~我們倉庫找無\n \n「' + keyWord + '」\n \n煩請填寫錯誤回報，\n感恩合十'
                print(text_)
                message = TextSendMessage(text = text_)
        
                # 刪除 file，以避免下次回報錯誤
                os.remove(path)
                print("### func.fuzzySearch.模糊搜尋.刪除file\n")

            line_bot_api.reply_message(event.reply_token,message) # 送出

    except:
        print("func.fuzzySearch.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def pushSearch(event):
    print("### func.pushSearch_start")
    print("### event.message.text: " + event.message.text )
    # 取得時間(至十分)
    ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
    time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
    print("### func.fuzzySearch." + time)
    # 存擋路徑
    path = Path() + event.source.user_id + "_" + time
    # 讀檔路徑
    pathForLoad = Path()
    try:
        import pandas as pd
        import numpy as np
      
        print("### func.pathForLoad.讀檔路徑:", pathForLoad)
        df = pd.read_csv(pathForLoad + '../RecommendSys/Food_Mixed2.csv', encoding='utf8') # 讀取資料
        df = df.drop_duplicates(subset='Braname', keep='first') # 刪除df['Name']重複值，並僅取第一
        df = df[['Braname', 'Intake_g', 'Cal_kcal', 'Protein_g', 'Fat_g', 'CHO_g']] # 僅取有需要的營養成分
        df = df.reset_index(drop=True) # 重整df_food_g之索引
        keyWord = event.message.text[12:-1]  # 搜尋關鍵字
 
        # 精準搜尋
        food = df[df['Braname'] == keyWord]

        print(food)
        if  len(food) == 1:
            print(food.iloc[0])
            i = food.iloc[0]
            food = ("品名："          +str(i[0]) + "\n" +
                    "食用量："        +str(i[1]) + "\n" +
                    "熱量(大卡)："    + str(i[2]) + "\n" +
                    "脂肪(克)："      + str(i[4]) + "\n" +
                    "蛋白質(克)："    + str(i[5]) + "\n" +
                    "碳水化合物(克)："+ str(i[3]) )
            text_ = "相關營養成分:\n \n" + food + "\n \n 吃吧吃吧~Ψ(￣∀￣)Ψ" #要印的語句
            print(text_)
            message = TextSendMessage(text = text_)

            line_bot_api.reply_message(event.reply_token,message) # 送出

        else:
            print('不要玩我啦!')
    except:
        print("func.pathForLoad.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
      

# 傳送嘴饞紀錄報告
def sendExtraFood(event):

    # 取得時間(至十分)
    ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
    time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
    print("### fun.sendExtraFood." + time)
    # 存擋路徑
    path = Path() + event.source.user_id + "_" + time    
    
    # 隨機生成回話內容 
    list = ["吃這麼好！\n 好啊！不分享啊！", "吃這麼好！\n 捏捏自己的肚子吧！", "哼哼！ ~\n我都記錄下來了！", "沒關係!\n 減肥是明天的事 "]
    feedBack = list[(random.randint(0,3))] 
    print("#### 回話: ", feedBack)   

    try:
        mtext = event.message.text
        print("### func.sendExtraFood_start\n")
        # 傳送錯誤回報給資料庫
        print("### func.sendExtraFood.我偷吃了一些小點心 (￣￢￣)給資料庫\n")
        print("傳送的資料：", mtext)
  




        # 刪除 file，以避免下次回報錯誤
        os.remove(path)
        print("### func.sendExtraFood.刪除file\n")

        # reponse
        print("### func.sendExtraFood.偷吃了：\n「" ,mtext,"\n" , feedBack, "_start")
        message = TextSendMessage(text = ("偷吃了：\n \n「"+ mtext  +"」\n \n"+ feedBack))
        print("### func.sendExtraFood.偷吃了：\n「", mtext, "\n", feedBack, "_end")
        line_bot_api.reply_message(event.reply_token,message)
        print("#######################")
    except:
        print("func.sendText.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


