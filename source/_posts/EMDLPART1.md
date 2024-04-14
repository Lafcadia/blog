---

title: 利用Requests和网易云音乐的API制作简单的网易云音乐下载器
date: 2022-05-15 09:50:34
tags: 
  - Python
  - 编程

---

## 一、前言与废话

这是个挺老的玩意了，我第一次尝试做这玩意的时候是在2018年我去千岛湖旅游的时候。

2022宅在温州乡下（想不宅也没办法，压根出不了家门），翻硬盘，翻到了这玩意，决定重写一遍

感觉这几年自己就没什么进步，估计退步了不少。

感觉天空的湛蓝也在为我的忧郁而忧郁。果然这个时候最想要飞翔在空中。但是在这种需要感情共鸣的时候，还不如听一首《魔法使的忧郁》。

果然是在想念谁，不然周围那么多人走过，自己怎么会感到孤单呢？
<!--more-->
## 二、代码（Python部分）

```python
from curses.ascii import isdigit
from sre_compile import isstring
import requests, json, sys, time, os
from you_get import common
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; rv:11.0) like Gecko"}

class TemplateError(Exception): #花里胡哨的一坨错误，自己当初怎么想的
    def __init__(self, err):
        print("程序出现了错误: "+err)
        Exception().__init__(self, err)
        
class FanMangError(TemplateError):
    def __init__(self, code):
        err = '网易云音乐出现了系统繁忙，请在几分钟之后重启程序。错误码: %s' % code
        super().__init__(self, err)

class NotExist404(TemplateError):
    def __init__(self):
        err = '您输入的ID指向不存在的音乐。'
        super().__init__(self, err)

class VIPMusicError(TemplateError):
    def __init__(self):
        err = '请使用网易云音乐APP下载VIP音乐。'
        super().__init__(err)

class IDError(TemplateError):
    def __init__(self):
        err = '错误的ID'
        super().__init__(self, err)

def IDTester(ID, ignorance=True):
    try:
        if isdigit(ID) == False and ignorance == False:
            print(f'ID:{ID}出现错误，请检查是否正确。')
            logWriter('出现了错误ID: '+ID+"，程序自动退出。", error=True)
            sys.exit(0)
        if isdigit(ID) == False and ignorance == True:
            logWriter('出现了错误ID: '+ID+"，程序未退出",error=True)
            ID = str(ID)
            raise IDError
        if isstring(ID) == False:
            ID = str(ID)
    except:
        print(f'ID:{ID}出现错误，请检查是否正确。')
    return ID

c = os.path.abspath('.')
def wyydownloader(ID, ignorance=True, where='.'):
    '''
    利用官方API实现。
    ID是一个字符串，是网易云音乐的歌曲ID，
    ignorance是一个是否被错误打断的boolean，若为True则忽视VIP歌曲无法下载错误并给予反馈。
    '''
    if os.getcwd() != c+where:
        os.chdir(where)
    ID = IDTester(ID)
    data = requests.get('http://music.163.com/api/song/detail/?id='+ID+'&ids=%5B'+ID+'%5D', headers=headers)
    if data.content == r'{"songs":[],"equalizers":{},"code":200}':
        raise NotExist404
    n = json.loads(data.content)
    state = n['songs'][0]['fee']
    if state == 1 and ignorance == False:
        raise VIPMusicError
    if state == 1 and ignorance == True:
        return 0
    name = n['songs'][0]['name']
    creator = n['songs'][0]['artists'][0]['name']
    chunk_size = 1024
    response = requests.get('http://music.163.com/song/media/outer/url?id=%s.mp3' % ID, headers=headers)
    file_size = response.headers.get('Content-Length')
    if file_size is not None:
        file_size = int(file_size)
    with open(f'{name} - {creator}.mp3', mode='wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)
    logWriter(f'ID为{ID}的歌曲下载成功。',error=False)

def searcher(name):
    f, c, d, k, _ = [], [], [], [], []
    data = requests.get(r'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={'+name+r'}&type=1&offset=0&total=true&limit=20',headers=headers)
    n = json.loads(data.content)['result']['songs'][0:9]
    for x in range(len(n)):
        f.append(n[x]['name'])
        c.append(n[x]['artists'][0]['name'])
        d.append(n[x]['id'])
    for y in range(len(n)):
        k.append([f[y],c[y],str(d[y])])
    for z in range(len(n)):
        _.append(('['+str(z)+']')+" | ".join(k[z]))
    for __ in range(len(n)):
        print(_[__])
    a = input('请输入你选择下载的歌曲: ')
    wyydownloader(str(d[int(a)]))

def album_web(ID):
    ID = IDTester(ID)
    url = "https://music.163.com/album?id=" + ID
    response = requests.get(url=url, headers=headers)
    html=response.content.decode(encoding="utf-8")
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('ul',{'class':'f-hide'})
    results=results.find_all('a')
    download = wyydownloader(results[0]['href'].split("=")[1],where='./'+ID)
    for music in results:
        try:
            download = wyydownloader(music['href'].split("=")[1])
            if download == 0:
                print('因VIP歌曲的版权原因，该歌曲无法下载。')
                logWriter('因VIP歌曲的原因无法下载ID为:{ID}的歌曲',error=True)
        except:
            print(f'第 {results.index(music)} 首歌曲的下载出现了问题')
            continue

def playlist_web(ID):
    ID = IDTester(ID)
    url = "https://music.163.com/playlist?id=" + ID
    response = requests.get(url=url, headers=headers)
    html=response.content.decode(encoding="utf-8")
    #print(html)
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('ul',{'class':'f-hide'})
    results=results.find_all('a')
    if os.path.exists(f'./{ID}') == False:
        os.makedirs(f'./{ID}')
    for music in results:
        try:
            download = wyydownloader(music['href'].split("=")[1],where=f'./{ID}')
            if download == 0:
                print('因VIP歌曲的版权原因，该歌曲无法下载。')
                logWriter('因VIP歌曲的原因无法下载ID为:{ID}的歌曲',error=True)
        except Exception as e:
            print(f'第 {results.index(music)} 首歌曲的下载出现了问题')
            print(e)
            continue

def playlist_full(ID): #不建议使用，网易云音乐的服务器的这个API常常挂机。
    ID = IDTester(ID)
    url = 'https://music.163.com/api/playlist/detail?id=' + ID
    response = requests.get(url=url, headers=headers)
    results = json.loads(response.content)
    if results['code'] == -447:
        raise FanMangError(results['code'])
    print(results)



def lyrics(ID):
    ID = IDTester(ID)
    try:
        url = 'http://music.163.com/api/song/media?id=' + ID
        data = json.loads(requests.get(url=url,headers=headers).content)
    except:
        print('您输入的ID指向不存在的音乐。')
    if 'lyric' in data:
        with open(ID+'.lrc', 'w') as f:
            f.write(data['lyric'])

# def getImg(ID):
#     data = requests.get('http://music.163.com/api/song/detail/?id='+ID+'&ids=%5B'+ID+'%5D', headers=headers)
#     n = json.loads(data.content)
#     url = n['songs'][0]['album']['picurl']
#     img = requests.get(url=url,headers=headers).content
#     with open('./img/'+ID+'.jpg','wb') as f:
#         f.write(img)

def logWriter(msg,error=True): #这个日志记录器也很失败
    if error == True:
        state = 'ERROR'
    else:
        state = 'INFO'
    with open('日志.log','a') as f:
        f.write(f'[{time.localtime(time.time())}][{state}]:'+msg)

# def addData(file, image): #这里本来想要写一个把专辑图片粘到mp3上去的函数的，想想算了，意义不大。
#     pass
if __name__ == '__main__':
    playlist_web('7266482854')
```

## 三、后语

在我写着这个东西的时候，我突然想起来有个东西叫you-get。

真是一出西西弗斯式的悲剧。但是我感觉我写的这个测出来的效率好像要比这个you-get高那么一点，可能是网速的问题？