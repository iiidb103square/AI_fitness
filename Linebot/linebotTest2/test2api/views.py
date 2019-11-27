from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, URIAction, ImageMessage, TextSendMessage, PostbackEvent, PostbackAction
from module import func, QuickReplyButton, sendCarousel,sendImage

from kafka import KafkaProducer, KafkaConsumer
import os, datetime, tempfile, json, re
from PAL import Path
from RecommendSys import BreakfastPush, LunchPush, DinnerPush

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    
    print("### callback.resquest: " , request)
    print("### callback.resquest傳輸的方式: ", request.method) 

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
                    
            print("### callback.resquest.POST.event(事件觸發格式): ", event)

            # 判斷使用者在linechat的對話之上一句是否為"'我要告御狀'"
            # 供告御狀的回覆用(elif mtext != "'我要告御狀'")
    
            # 取得時間(至十分)
            ISOTIMEFORMAT = '%Y%m%d%H%M' # 指定時間格式
            time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))[:-1]
            print("### callback.time: " + time)
            # 存擋路徑
            path = Path() + event.source.user_id + "_" + time
            print("###存檔路徑:",  path[:-11])
     
            # :讀取暫存檔內容
            if os.path.isfile(path):
                f = open(path)
                text = f.readlines()
                f.close()
                print("### callback" +str(text))

            # Postback事件觸發
            if isinstance(event, PostbackEvent):
                print("### callback.isinstanc.Postback觸發_start")
                print("### event.postback.data:" ,event.postback.data)  
                if event.postback.data  == 'fuzzySearch':
                    print("### callbacki.isinstance.PostbackEvent.fuzzySearch_start")

                    # 創建file，供func.sendText.ExtraFood使用
                    f  = open(path,"w")
                    f.write('ExtraFood') #####內文為'嘴饞紀錄'
                    f.close
                    #print("### func.UserData."吃了什麼跟我說說")
                    message = TextSendMessage(text = "吃了什麼跟我說說\n(打在對話框送出即可)")
                    #print("### func.UserData."吃了什麼跟我說說")
                    line_bot_api.reply_message(event.reply_token,message)
                    print("### func.UserData.吃了什麼跟我說說")

            # 事件觸發
            if isinstance(event, MessageEvent):
                print("### callback.isinstanc.事件觸發")
                
                # 照片事件觸發
                if isinstance(event.message, ImageMessage) and (os.path.isfile(path)) and text == ['img']:
                    os.remove(path) # 刪除資料夾，避免干擾

                    print("### callback.isinstanc.照片事件觸發_start")
                    message_content = line_bot_api.get_message_content(event.message.id)                  
                    print("### callback.isinstanc.照片事件觸發.message_content",  message_content)
                    sendImage.Image(event)
                    print("### callback.isinstanc.照片事件觸發_end")
                    #line_bot_api.reply_message(event.reply_token, message) 

                # 文字事件觸發
                if isinstance(event.message, TextMessage):
                    print("### callback.isinstanc.文字事件觸發")

                    mimange = event.message
                    print("### event.message:", (event.message))
                    print("### TextMessage:", TextMessage)
                    #文字訊息
                    mtext = event.message.text

                    print("### views.callback_start\n")                
                    print("### callback.isinstanc.文字事件觸發,輸入訊息:" + mtext)



                 # testi 問卷用 
                    if mtext[:3] == "###":
                        os.remove(path) # 刪除資料夾，避免干擾

                        print("### views.callback.問卷_start\n")
                        list_ = ["userId", "sex", "age", "height", "weight", "bodyFat", "exerciseFrequency"]
                        QA = 5
                        #message = (event.source.user_id + "/"+ mtext[3:]+ "/" + time) 
                        message = (mtext)
                        print(message, "_end")
                        print(type(message))
                        from kafka import KafkaProducer
                        producer = KafkaProducer(bootstrap_servers=['35.221.199.161:9092'])
                        future = producer.send('ttt', bytes(mtext, encoding="utf8"))
                        result = future.get(timeout=30)
                       
                        line_bot_api.reply_message(event.reply_token,message)
                        #json.load(filename)
                        #json.loadds(string)     


          
                # 圖文選單
                    if mtext == "我升級了，我要更新狀態值 ლ(´ڡ`ლ)":
                        print("### views.callback.'基本資料'\n")
                        if os.path.isfile(path):  # 為避免暫存檔干擾
                            os.remove(path)

                        QuickReplyButton.UserData(event)
                    
                    elif mtext == '人家要吃飯飯~ ♥(´∀` )':
                        print("### callback.time(hr).'人家要吃飯飯~ ♥(´∀` )'")
                           
                        # 取得時間(hr)
                        ISOTIMEFORMAT = '%H' # 指定時間格式
                        time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))
                        print("### callback.time.'人家要吃飯飯~ ♥(´∀` )': " + time)
            
                        if 10 >= int(time) >= 4:
                            BreakfastPush.BreakfastPush(event)
                        elif 17  > int(time) > 10:
                            LunchPush.LunchPush(event)
                        elif 23  > int(time) >= 17:
                            DinnerPush.DinnerPush(event) 
                        else:
                            message = TextSendMessage(text = "乖~這時候就別吃了吧~")
                            print("### views.callback.'乖~這這時候就別吃了吧~'_start\n")   
                            line_bot_api.reply_message(event.reply_token,message)
                            print("### views.callback.'乖~這這時候就別吃了吧~'_end\n")

                    elif mtext == "人家想知道吃進了多少熱量嘛~ (￣￢￣)~":
                        print("### views.callback.人家想知道吃進了多少熱量嘛~ (￣￢￣)~_start\n")
                        func.sendText(event)
                        print("### views.callback.人家想知道吃進了多少熱量嘛~ (￣￢￣)~_end\n")

                    elif mtext == "我鼓起勇氣，面對過去的自己 (*•̀ㅂ•́)ﻭ":
                        print("### views.callback.'我鼓起勇氣，面對過去的自己 (*•̀ㅂ•́)ﻭ'_start\n")
                        if os.path.isfile(path):  # 為避免暫存檔干擾
                            os.remove(path)

                        func.sendText(event)
                        print("### views.callback.'我鼓起勇氣，面對過去的自己 (*•̀ㅂ•́)ﻭ'_end\n")

                    elif mtext == "呼叫姿勢王 ٩(♡ε♡ )۶":

                        if os.path.isfile(path):  # 為避免暫存檔干擾
                            os.remove(path)

                        sendCarousel.Pose(event)
    
                    elif mtext == '我不想再當單身狗了(〓￣(∵エ∵)￣〓)':
                        print("### views.callback.我不想再當單身狗了_start\n")                
                        if os.path.isfile(path):  # 為避免暫存檔干擾
                            os.remove(path)

                        func.sendText(event)
                        print("### views.callback.我不想再當單身狗了(〓￣(∵エ∵)￣〓)_end\n")
                                                
   
                    elif mtext == "我要告狀！(╬ಠ益ಠ)":
                        print("### views.callback.我要告狀！(╬ಠ益ಠ)_start\n") 
                        func.sendText(event) 
                        print("### views.callback.我要告狀！(╬ಠ益ಠ)_end\n")

                # 基本資料之快速選單的回覆 
                    elif mtext == "讓我記錄這美好的body吧~":
                        print("### views.callback.讓我記錄這美好的body吧~")
                        func.sendText(event)

               
                # 告御狀的回覆
                    elif mtext != "我要告狀！(╬ಠ益ಠ)" and (os.path.isfile(path)) and text == ['ErrorReport']:    
                        print("### views.callback.mtext != '我要告御狀'_start\n") 
                        func.sendErrorReport(event)
                        print("### views.callback.mtext != '我要告御狀'_end\n")

                # 嘴饞紀錄的回覆
                    elif mtext != "人家想知道吃進了多少熱量嘛~ (￣￢￣)~" and (os.path.isfile(path)) and  text == ['ExtraFood']:
                        print("### views.callback.mtext != 人家想知道吃進了多少熱量嘛~ _start\n")
                        func.fuzzySearch(event)
                        print("### views.callback.mtext != 人家想知道吃進了多少熱量嘛~ (￣￢￣)~_end\n")

                # 飲食建議回覆    
                    elif mtext[:9] == "我想吃查理大師的 ": 
                        print("### views.callback.mtext =" + mtext[:9] + " _start")
                        func.pushSearch(event)
                        print("### views.callback.mtext =" + mtext[:9] + " _start")

                return HttpResponse()
                print("### view.callback_end\n")   
    else:
        return HttpResponseBadRequest()


