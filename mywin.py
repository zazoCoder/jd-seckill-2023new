import datetime
import threading
import time
import sys
import os
from tkinter.scrolledtext import ScrolledText

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from multiprocessing import Process
import requests

from jd.tools import utils
from jd.JDMain import JDSecKillSubmit
from jd.api_timer import JDTimer
import tkinter.messagebox
from tkinter import *


def syncTime():
    jdTimer = JDTimer()
    return jdTimer.local_jd_time_diff()


def yuyueSku(sku, ck):
    jdapi = JDSecKillSubmit(sku, ck)
    jdapi.setLogText(scrollText)
    jdapi.appoint_task()


def killSku(sku, ck, killTimeTs):
    jdapi = JDSecKillSubmit(sku, ck)
    jdapi.setLogText(scrollText)
    for i in range(5):
        print('第%d次kill---------------------------->' % i)
        if jdapi.killSku(killTimeTs):
            break


def work(killTime, ck, sku):
    killTimeTs = utils.getTimeStamp(killTime, format='%Y-%m-%d %H:%M:%S.%f')

    syncedTime = False
    hasYuyue = False

    timeDiff = 0  # 时差

    lastLogTimeTs = 0

    while True:
        nowTimeTs = int(time.time() * 1000)
        killDiff = killTimeTs - nowTimeTs
        print("时间剩余%s秒" % str(int(killDiff / 1000)))
        if nowTimeTs - lastLogTimeTs > 1000:
            lastLogTimeTs = nowTimeTs
            scrollText.insert(END, "\n距离抢购剩余%s秒" % str(int(killDiff / 1000)))
            scrollText.see(END)

        if killDiff < 5 * 60 * 1000 and not syncedTime:
            syncedTime = True
            timeDiff = syncTime()
            print("时差：%s" % str(timeDiff))
            killTimeTs = killTimeTs + timeDiff
        elif killDiff < 2 * 60 * 1000 and not hasYuyue:
            hasYuyue = True
            yuyueSku(sku=sku, ck=ck)
        elif killDiff < 0:
            print("时差：%s" % str(timeDiff))
            killSku(sku=sku, ck=ck, killTimeTs=killTimeTs)
            break
        time.sleep(0.01)


def make_app():
    app = Tk()
    width = 800
    heigh = 470
    screenwidth = app.winfo_screenwidth()
    screenheight = app.winfo_screenheight()
    app.geometry('%dx%d+%d+%d' % (width, heigh, (screenwidth - width) / 2, (screenheight - heigh) / 2))
    app.title('jd抢购试用版')
    Label(app, text='cookie').place(relx=0.1, rely=0.05)
    cookieStr = StringVar()
    ck = 'pin=duanhunj;wskey=AAJi-m1JAEBW4OiTFVIUTSSbujpUFgc1pSuTOSBffOXPlCmbe5pU2PnGUbkmuYLMyIidblYF4FMif3fChvflaarG7JUYb_gm;whwswswws=qM-2abFlgSy4tbYsg9WW1IbEslu48p6FVbfDVxzWNH7nMFArasiOuf_OsHMKPHBVPRlIBl5EP-e53vM1FTUcuwCPHuiK5229xxvu4rQ3Gz5rHd-S5qqeDEGdZn3rVF9db;unionwsws={"devicefinger":"eidA0e948122b9s5NiiX6oi9SCuxIh0tzw+cujYomW0q9ZMeyYYd9u9p34ib2JzxKPNP0EFhBJSsCjbYjBjS12VDNfFi7PYWPqlRbDCvSkAQDwpZZpJF","jmafinger":"qM-2abFlgSy4tbYsg9WW1IbEslu48p6FVbfDVxzWNH7nMFArasiOuf_OsHMKPHBVPRlIBl5EP-e53vM1FTUcuwCPHuiK5229xxvu4rQ3Gz5rHd-S5qqeDEGdZn3rVF9db"};'
    cookieStr.set(ck)
    cookieStr.set('')
    Entry(app, textvariable=cookieStr, name='cookie').place(relx=0.1,
                                                            rely=0.1,
                                                            relwidth=0.8,
                                                            relheight=0.1)

    Label(app, text='输入抢购时间').place(relx=0.1, rely=0.25)
    timeStr = StringVar()
    timeStr.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23])
    Entry(app, textvariable=timeStr, name='ipt').place(relx=0.1,
                                                       rely=0.30,
                                                       relwidth=0.3,
                                                       relheight=0.1)

    Label(app, text='商品ID').place(relx=0.45, rely=0.25)
    pId = StringVar()
    # pId.set('2148924,10026899941091,100013490678')  #
    pId.set('100012043978')  # sku
    Entry(app, textvariable=pId, name='ipt1').place(relx=0.45,
                                                    rely=0.30,
                                                    relwidth=0.2,
                                                    relheight=0.1)

    Label(app, text='数量').place(relx=0.7, rely=0.25)
    count = StringVar()
    count.set('1')
    Entry(app, textvariable=count, name='ipt2').place(relx=0.7,
                                                      rely=0.30,
                                                      relwidth=0.2,
                                                      relheight=0.1)

    Button(app, text='点击开始抢购', fg="black", bg="white",
           command=start).place(relx=0.1,
                                rely=0.45,
                                relwidth=0.8,
                                relheight=0.1)

    scrollText = ScrolledText(app)
    scrollText.place(relx=0.1,
                     rely=0.60,
                     relwidth=0.8,
                     relheight=0.3)
    scrollText.insert(END, '步骤：')
    scrollText.insert(END, '\n第一步：手机抓包cookie，将cookie填到cookie框')
    scrollText.insert(END, '\n第二步：填抢购时间、抢购时间')
    scrollText.insert(END, '\n第三步：点击抢购按钮')

    Label(app, text='问题咨询QQ：285126081').place(relx=0.1, rely=0.95)

    return app, scrollText


def start():
    sku = app.children['ipt1'].get()
    killTime = app.children['ipt'].get()
    ck = app.children['cookie'].get()

    t = threading.Thread(target=work, args=(killTime, ck, sku))
    t.setDaemon(True)
    t.start()


app, scrollText = make_app()
app.mainloop()
