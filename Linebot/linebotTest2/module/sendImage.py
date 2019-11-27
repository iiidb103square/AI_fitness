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

from linebot.models import TextSendMessage,  ImageMessage, ImageComponent, ImageSendMessage
import tempfile

import os, datetime
from PAL import Path 
from kafka import KafkaProducer, KafkaConsumer
from module import bodyType

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def Image(event):
    try:
        # 處理數位影像片事件觸發
        print("### module.sendImage.Image.處理數位影像片事件觸發_start")
        # 儲存格式
        ext = 'jpg'

        # message_content = line_bot_api.get_message_content(event.message.id)
        print("### module.sendImage.Image.處理數位影像片事件觸發.message_content")

        # 取得現在時間(至日)
        ISOTIMEFORMAT = '%Y%m%d%H%M%S' # 指定時間格式 #'%Y%m%d%H%M'
        time = (datetime.datetime.now().strftime(ISOTIMEFORMAT))
        print("### module.sendImage.Image.現在日期:" + time)

        # 儲存檔案名：user_id + 日期
        fileName = "BodyPhoto_" + event.source.user_id + "_" + time  
        print("### module.sendImage.Image.儲存檔名:" + fileName)       
        
        #儲存路徑
        path  = Path()
        print("### module.sendImage.Image.儲存路徑:" + path)
        
        message_content = line_bot_api.get_message_content(event.message.id)

        # 將圖片存在本地端
        print("### module.sendImage.Image.with tempfile.NamedTemporaryFile")
        with tempfile.NamedTemporaryFile(dir=path, prefix=fileName + "." + ext, delete=False) as tf: # delete = False, 使得檔案不會用完就刪
            print("### module.sendImage.Image.with tempfile.module.chunk")

            for chunk in message_content.iter_content():
                tf.write(chunk)
            path = tf.name

            dist_path = path[:-8] # 新檔名 == 將舊檔名後8碼(亂碼?)去除
            dist_name = os.path.basename(dist_path) 
            os.rename(path, dist_path) # 重新命名

            import base64
            f=open(dist_path,'rb')
            imageString = base64.b64encode(f.read())
            f.close()
        os.remove(dist_path)  # 刪除照片檔 
       
        print("### module.sendImage.Image.將圖片直送kafka.try")
        try:  
            # 將圖片直送kafaka
            print("### module.sendImage.Image.將圖片直送kafka")

            from PAL import kafkaIPandPort, kafkaTopic #不知道為什麼一定要放在才能運行   
    
            kafkaIPandPort = kafkaIPandPort()
            print("### kafkaIPandPort: ", kafkaIPandPort)
            kafkaTopic= kafkaTopic()
            producer = KafkaProducer(bootstrap_servers=[kafkaIPandPort])

            # kafka producer
            print("### module.sendImage.Image.producer_start")
            future = producer.send(kafkaTopic , key= bytes((event.source.user_id+time),encoding='utf8'), value= imageString, partition= 0) 
            result = future.get(timeout=30)
            print("### module.sendImage.Image.producer_end")
  
            # kafka consumer
            print("### module.sendImage.Image.comsumer_start")
            consumer = KafkaConsumer('t_ti', bootstrap_servers= [kafkaIPandPort])
            print("### module.sendImage.Image.comsumer: 迴圈開始")

            for bodysize in consumer:
                bodysize = bodysize
                print("### module.sendImage.Image.comsumer.體態類型")
                print("### kafka回傳的value:", bodysize[6])

                bodysize_String = bodysize[6].decode() #抓出kafka回傳的value，並轉從2進制轉成字串
                print("### 體態類型[6].bodysize_String:", bodysize_String) 

                if bodysize_String == 'S' or bodysize_String == 'M' or bodysize_String == 'L': #判別體態
                    print("### module.sendImage.Image.comsumer.體態類型.break")
                    break  # 如果有抓到資料就跳出迴圈

            print("### module.sendImage.Image.comsumer_end")

        except:
            print("### module.sendImage.Image.將圖片直送kafka.except")
            pass 
       
        print("### module.sendImage.Image.bodysize_String.bodyType_start")

        from module import bodyType
        bodyType = bodyType.bodyType(bodysize_String)
        print("### module.sendImage.Image.bodysize_String.bodyType: " + bodyType)

        print("### module.sendImage.Image.bodysize_String.text: " + bodysize_String)
        text = ("你的體型為: " + bodysize_String + "\n體態為: " + bodyType)

        line_bot_api.reply_message(
            event.reply_token, [
                #ImageSendMessage(url= "line://app/1653356616-2QDQMDzj"),
                TextSendMessage(text)
            ])
        print("### event.message:", text)

    except:        
        print("### sendImage.Image.發生錯誤")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

