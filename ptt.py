import requests
# from urllib.error import HTTPError
import os
import json
from bs4 import BeautifulSoup

page = 1
howmany = 20
total = []

for s in range(howmany):
    url = "https://www.ptt.cc/bbs/MuscleBeach/search?page=" + str(page + s) + "&q=課表"
    response = requests.get(url).text
    # print(response.text)
    html = BeautifulSoup(response)
    for t in html.find_all("div", class_="title"):
        # 沒有a代表被刪除
        if not t.find("a") == None:
            turl = "https://www.ptt.cc" + t.find("a")["href"]
            total.append(turl)

for u in total:
    url = u
    response = requests.get(url).text
    html = BeautifulSoup(response)
    metas = html.find_all("span", class_="article-meta-value")

    if not len(metas) < 4:
        print("ID:", metas[0].text)
        print("看板:", metas[1].text)
        print("標題:", metas[2].text)
        print("時間:", metas[3].text)

        score = 0
        pushes = html.find_all("span", class_="push-tag")
        for p in pushes:
            if "推" in p.text:
                score = score + 1
            elif "噓" in p.text:
                score = score - 1
        print("推噓文分數:", score)

        saved = {"id": metas[0].text,
                 "board": metas[1].text,
                 "title": metas[2].text,
                 "time": metas[3].text,
                 "score": score}

        notallowed = ["/", "|", "\\", "?", "\"", "*", ":", "<", ">", ".", "！", " ", "？"]
        title_revised = ""

        for c in metas[2].text:
            if not c in notallowed:
                title_revised = title_revised + c
        dn = "ptt/" + title_revised
        if not os.path.exists(dn):
            os.makedirs(dn)

    for i, a in enumerate(html.find_all("a")):
        allow = ["gif", "jpg", "jpeg", "png"]
        if a["href"].split(".")[-1].lower() in allow:
            print("GET:", a["href"])
            # .raw(圖片...): stream = True
            img_response = requests.get(a["href"], stream=True)
            img = img_response.raw.read()

            dn = "ptt/" + title_revised
            fn = dn + "/" + str(i) + "." + a["href"].split(".")[-1]
            f = open(fn, "wb")
            f.write(img)
            f.close()


    # 內文部分
    content = html.find("div", id="main-content")
    ds = content.find_all("div", class_="article-metaline")
    for d in ds:
        d.extract()
    ds = content.find_all("div", class_="article-metaline-right")
    for d in ds:
        d.extract()
    ds = content.find_all("div", class_="push")
    for d in ds:
        d.extract()
    print("內文:", content.text)
    saved["content"] = content.text


    # 儲存內文(JSON)
    dn = "ptt/" + title_revised
    f = open(dn + "/meta.json", "w", encoding="utf-8")
    json.dump(saved, f)
    f.close()
    print("-" * 20)


