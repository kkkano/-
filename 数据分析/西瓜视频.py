"""
[课题]: Python爬取西瓜视频
[授课老师]: 青灯教育-巳月 
录播链接: https://pan.baidu.com/s/12nTTkcrL-RcGgFOipZ8dyQ?pwd=g58i 提取码: g58i
"""
import base64
import re
import requests
import os


def getUrl(id_):
    url = "https://www.ixigua.com/" + id_
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Dest": "document",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Referer": "https://www.ixigua.com/7025900714182476299",
        # "Cookie":"__ac_nonce=06122217b0057aec2e7ce; __ac_signature=_02B4Z6wo00f01HiyszAAAIDBG7hzW.3penR4kreAAH8W6f; __ac_referer=__ac_blank; ttcid=5d55ea80f73040bc8f7c1211ed58458a48; MONITOR_WEB_ID=50984067-b35f-484a-a7dd-bed58d13bc71; ttwid=1%7Cb3BvZjY5ybfG0cQfXCc00jjr8rQnM8aSZL8WE6BdLu8%7C1629626748%7C14ca7b64258bf402324c3cdee546221029a261bb6a3a3d34fe353682f41e49a2"
    }
    session = requests.session()
    # 需要先访问一次视频网站获取cookies才行
    session.get(url, headers=headers)
    result = session.get(url + "?wid_try=1", headers=headers)
    result.encoding = "UTF-8"
    # print(result.text)
    title = re.findall('<title data-react-helmet="true">(.*?)</title>', result.text)[0]
    title = title.replace(' ', '').replace('️', '')
    title = re.sub(r'[\/:*?"<>|]', '', title)
    vt = re.search(r'definition":"1080p"[\s|\S]*?main_url":"(?P<main_url>.*?)"', result.text, re.S)
    at = re.search(r'dynamic_audio_list":\[{"quality":"normal"[\s|\S]*?main_url":"(?P<main_url>.*?)"', result.text, re.S)
    audio_url = base64.b64decode(at.group("main_url")).decode("utf-8")
    video_url = base64.b64decode(vt.group("main_url"))
    video_url = str(video_url).replace(r".\xd3M\x85", "?")[2:-1]
    audio_data = requests.get(audio_url).content
    with open(f'audio/{title}.mp3', mode='wb') as f:
        f.write(audio_data)
    print(f"{title}音频下载完成")
    video_data = requests.get(video_url).content
    with open(f'video/{title}1.mp4', mode='wb') as f:
        f.write(video_data)
    print(f"{title}1视频下载完成")
    merge(title+'.mp3', title+'1.mp4', title+'.mp4')


def merge(audio_title, video_title, title):
    ffmpeg = r'D:\Download\ffmpeg\bin\ffmpeg.exe -i ' + 'video/' +video_title + ' -i ' + 'audio/' +audio_title + ' -acodec copy -vcodec copy ' + "out/" + title
    # print(ffmpeg)
    os.popen(ffmpeg)

getUrl("7033698012861825550")