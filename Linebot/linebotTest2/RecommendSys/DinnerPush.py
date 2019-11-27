from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

import csv
import pandas as pd
import random
from PAL import Path
from RecommendSys import PushFood, PushFood2

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

path = Path()

def DinnerPush(event):
    df = pd.read_csv(path + '../RecommendSys/Personal_data.csv', encoding='utf8')
    # 輸入基本資料
    Gender = df['性別'][0]
    Age = df['年齡'][0]
    Height = df['身高'][0]
    Weight = df['體重'][0]
    # print(Gender, Height, Weight, Age)
    # 計算 BMR
    if Gender == 0:
        BMR = 10*Weight + 6.25*Height - 5*Age + 5
    else:
        BMR = 10*Weight + 6.25*Height - 5*Age - 161
    # print(BMR)
    # 計算TDEE
    ActLevel = df['活動程度'][0]
    posture = df['體態'][0]
    p = posture


    if ActLevel == 1:
        TDEE = BMR * 1.2
    elif ActLevel == 2:
        TDEE = BMR * 1.375
    elif ActLevel == 3:
        TDEE = BMR * 1.55
    elif ActLevel == 4:
        TDEE = BMR * 1.725
    else:
        TDEE = BMR * 1.9

    # 搭配體態增肌或減脂
    if p in (1, 2, 3):
        FTDEE = round(TDEE * 0.9)
    elif p in (4, 7, 8):
        FTDEE = round(TDEE * 1.07)
    else:
        FTDEE = round(TDEE)
    # print(FTDEE)
    # 計算一天的量
    CHO_day = FTDEE * 0.5/4
    protein_day = FTDEE * 0.3/4
    Fat_day = FTDEE * 0.2/9
    # print(CHO_day, protein_day, Fat_day)

    # 計算一餐的量

    # 晚餐
    Kcal_dinner = FTDEE * 0.4
    CHO_dinner = round(CHO_day * 0.4)
    protein_dinner = round(protein_day * 0.4)
    Fat_dinner = round(Fat_day * 0.4)
    # print("Dinner:", "Kcal=", Kcal_dinner, "CHO_g=", CHO_dinner, "g,", "Pro_g=", protein_dinner, "g,", "Fat_g=", Fat_dinner, "g")

    # 讀取csv
    # df = pd.read_csv("Food_Mixed2.csv", encoding='utf8')
    df = pd.read_csv(path + '../RecommendSys/Food_Mixed2.csv', usecols=['FoodLabel', 'Breakfast', 'Lunch', 'Dinner', 'Recommend', 'Braname', 'Cal_kcal', 'Intake_g', 'CHO_g', 'Fat_g', 'Protein_g'], encoding='utf8')
    # 設定條件
    # 晚餐
    condition1 = df['Recommend'].astype(float) == 1
    condition2 = df['Dinner'].astype(float) == 1
    condition3 = df['FoodLabel'].astype(float) == 1
    condition4 = df['Cal_kcal'].astype(float) <= Kcal_dinner
    condition5 = (df['CHO_g'].astype(float) > CHO_dinner * 0.5) & (df['CHO_g'].astype(float) <= CHO_dinner)
    condition6 = (df['Fat_g'].astype(float) > Fat_dinner * 0.5) & (df['Fat_g'].astype(float) <= Fat_dinner)
    condition7 = df['Protein_g'].astype(float) > protein_dinner * 0.5



    Com = df[condition1 & condition2 & condition3 & condition4 & condition5 & condition6 & condition7]
    df2 = Com.sort_values(by="Cal_kcal", ascending=False)
    show2 = df2.sample(n=3, replace=False, random_state=None, axis=None)
    print(show2[['Braname']])
    print("-----------------------------")

    details = show2.loc[:, ['Braname', 'Intake_g', 'Cal_kcal', 'CHO_g', 'Fat_g', 'Protein_g']]
    details.rename(columns={'Braname':'品名', 'Intake_g':'食用量', 'Cal_kcal':'熱量(大卡)', 'CHO_g':'碳水化合物(克)', 'Fat_g':'脂肪(克)', 'Protein_g':'蛋白質(克)'}, inplace=True)

    # 避免飲食建議重複，寫次判別式
    if details.iloc[0][0] == details.iloc[1][0] or details.iloc[0][0] == details.iloc[2][0] or details.iloc[1][0] == details.iloc[2][0]:
        print("飲食建議重複了，再來一次")
        DinnerPush(event)

    else:
        print('---------------------------------')
        print(details.iloc[0])
        print('---------------------------------')
        print(details.iloc[1])
        print('---------------------------------')
        print(details.iloc[2])
        Push = [details.iloc[0], details.iloc[1], details.iloc[2]] # 欲推薦餐點
        print(Push) 
        PushFood2.PushFood2(event, Push)        
                   

