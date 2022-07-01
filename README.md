# 哔哩哔哩小程序转视频快照 for Hoshino
<br>这是一个HoshinoBot插件</br>
<br>实现功能：把群友发的哔哩哔哩小程序转成预览图，方便懒得看的懒狗们</br>
<br>视频部分引用了bilibili_api项目，项目地址：<url>https://github.com/Nemo2011/bilibili_api</url></br>

# 具体功能
<br>将群聊中的哔哩哔哩小程序视频，将低于十分钟的视频生成预览图（九宫格类型），大于十分钟类型的视频生成视频快照（基于bilibili开放api）并发送至群聊</br>

# 使用教程
<br>本模块引入了moviepy，opencv-python及bilibili-api-python模块</br>
```
   pip install moviepy
   pip install opencv-python
   pip install bilibili-api-python
```
<br>和其他插件一样 git后在config中增加bilivedioSnap模块，重启hoshino即可</br>

# 可调参数
<br><b>采用快照的边界时间</b></br>
`if totaltime < 600:  #边界时间` 其中单位为秒
<br><b>预览图的子图数量</b></br>
```
    rows = 4  #行数
    cols = 4  #列数
```
<br>设置列数行数即可</br>

# 可能存在的bug
1. 带有哔哩哔哩的消息可能会发生不知道什么样的错误，也有可能不会发生
2. 我也不知道会发生什么
