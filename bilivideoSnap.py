import math
import os
import asyncio
from bilibili_api import video, Credential, HEADERS
import aiohttp
import requests
import re
from hoshino import Service, R
from aiocqhttp.message import MessageSegment
from hoshino import aiorequests
from moviepy.editor import *
from moviepy.editor import *
import os
import cv2
import numpy as np

sv = Service('bilivideoSnap', enable_on_default=True)

def check(msg):
    if re.search(r"bilibili.com/video",msg) is not None:
        return 1
    elif re.search(r"哔哩哔哩",msg) is not None:
        return 2
    else:
        return 3
def getbvid(msg):
    rep = r"www.bilibili.com/video/.{12}"
    bvid = re.search(rep,msg).group()[-12:]
    return bvid

async def geturl(msg):
    header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
    print(msg)
    reprin = r"https:\\/\\/b23.tv\\/.{7}" #qq转qq
    repri2 = r"https://b23.tv/.{7}"#bilibiliHD qq小程序
    repri3 = r"https.+\?"
    try:
        a = re.search(repri2,msg).group()[-7:]
    except:
        a = re.search(reprin,msg).group()[-7:]
    url  = f"http://b23.tv/" + a
    res  = await aiorequests.get(url,headers=header,verify=False)
    bvurl = re.match(repri3,res.url).group()
    bvid = re.search(r"BV.+",bvurl).group()[:-1]
    if bvid[-1] == "/":
        bvid = bvid[:-1]
    return bvid

async def check_time(bvid):
    header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
    url = "http://api.bilibili.com/x/player/videoshot?bvid={}".format(bvid)
    url2 = "http://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid)
    res = await aiorequests.get(url, headers=header)
    js = await res.json()
    res2 = await aiorequests.get(url2, headers=header)
    js2 = await res2.json()
    totaltime = js2["data"]["duration"]
    if totaltime < 600:  #边界时间
        return False
    imgurl = f"http:" + js["data"]["image"][0] #获取快照
    img = requests.get(imgurl).content
    with open("img.jpg", 'wb') as f:
        print(1)
        f.write(img)
    return True

async def download_video(BVID):
    SESSDATA = "312f975f%2C1678682145%2C86109%2A91"
    BILI_JCT = "0b504a917cb834947a03508ca80a50c1"
    BUVID3 = "DE7BA6D3-74E4-438F-AACA-4F28BDD6E12E53950infoc"
    # 实例化 Credential 类
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    # 实例化 Video 类
    v = video.Video(bvid=BVID, credential=credential)
    # 获取视频下载链接
    url = await v.get_download_url(0)
    # 视频轨链接
    video_url = url["dash"]["video"][0]['baseUrl']
    async with aiohttp.ClientSession() as sess:
        # 下载视频流
        async with sess.get(video_url, headers=HEADERS) as resp:
            length = resp.headers.get('content-length')
            with open('video.mp4', 'wb') as f:
                process = 0
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    process += len(chunk)
                    f.write(chunk)
        print('已下载为：video.mp4')

async def getpic():
    video = VideoFileClip('video.mp4')
    total_time = video.duration
    rows = 4  #行数
    cols = 4  #列数
    frames = rows*cols  #要放多少个图片
    time_delta = total_time /frames
    time = 0
    dir='./videoimg/'
    imglist = []
    hlist = []
    for i in range(frames):
        col = i % cols
        filename = os.path.join(dir + str(i) + '.jpg')
        video.save_frame(filename, t=time)
        time = time + time_delta
        img = cv2.imread(filename)
        imglist.append(img)
        if col == cols-1: #到达末尾
            hlist.append(np.hstack(imglist))
            imglist.clear()
        if i == frames-1: #遍历完了
            img = np.vstack(hlist)
            cv2.imwrite("fin.jpg", img)
    video.close()
    #os.remove('./video.mp4')

@sv.on_message('group')
async def pulipuli(bot,event):
    msg = str(event.message)
    if check(msg) == 3:
        return
    if not os.path.exists('./videoimg'):
        os.mkdir('./videoimg')
    bvid = ""
    if check(msg) == 2: #处理小程序
        bvid = await geturl(msg)
    if check(msg) == 1: #处理普通链接\
        bvid = getbvid(msg)
    flag = await check_time(bvid)
    if flag == False:
        await download_video(bvid)
        await getpic()
        path = os.getcwd() + "\\" + "fin.jpg"
    else:
        path = os.getcwd() + "\\" + "img.jpg"
    await bot.send(event,f"[CQ:image,file=file:///{path}]")