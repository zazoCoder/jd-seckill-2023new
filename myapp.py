import time
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from multiprocessing import Process
import requests

from jd.tools import utils
from jd.JDMain import JDSecKillSubmit
from jd.api_timer import JDTimer



def syncTime():
    jdTimer = JDTimer()
    return jdTimer.local_jd_time_diff()


def yuyueSku(sku, ck):
    jdapi = JDSecKillSubmit(sku, ck)
    jdapi.appoint_task()


def killSku(sku, ck, killTimeTs):
    jdapi = JDSecKillSubmit(sku, ck)
    for i in range(5):
        print('第%d次kill---------------------------->' % i)
        if jdapi.killSku(killTimeTs):
            break

def work(killTime, ck, sku):
    print('ck:', ck)
    killTimeTs = utils.getTimeStamp(killTime, format='%Y-%m-%d %H:%M:%S.%f')

    syncedTime = False
    hasYuyue = False

    timeDiff = 0  # 时差

    while True:
        nowTimeTs = int(time.time() * 1000)
        killDiff = killTimeTs - nowTimeTs
        print("时间剩余%s秒" % str(int(killDiff / 1000)))

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


if __name__ == '__main__':

    sku = '100012043978'

	# 抢购时间
    killTime = '2023-06-01 11:59:59.800'

	# cookie
    cks = [
        'pin=jd_41d74c83f8224;wskey=AAJjKGIcAED51MS4xl3rMhkuKoz3aIdtHgYbbY_gONAtDcvoXgp0nCjPWKcjgXoBw3ZNcm-HVECeryK5NBFQiErqyGbAcqt-;whwswswws=JD012145b9WBZ52FxcoJ166359098310502j1UGQOp_xw1sHnZf2TBLxIAVcI1pr_ptSG7GbI4Jh8JHPzpgXIVd6vHgcp4KUP7bIcL92ot4SobMNdIjsb6CeO0xXfdGg1DB166dh3n~lV6zvij0xVW8O87RwFvqyq8bfocRq2uG0yIAc6GJfPzG3Vt7W-bSkl68yzw3cggRUZpEKUJ0VpkW0x0Q0aGrCFLasnWujHANJMp2D1tUHzbtF-NKQkCBUiGE1ZKdTwYkeVoNQaOoU87ivURTKramyPzaIW67BRI6kPNkr3PLHsHc;unionwsws={"devicefinger":"eidAfa90812247s5vgf0CkxeRgeWBZfWowyK9r4H9Y2h1wPWRDa\/+LyYAJea3ooTv4ePNmFFv1ZArvKR74Nk1rlZWoaTpHUgZCeqmC5Lix6Hz1eGUEN6","jmafinger":"JD012145b9WBZ52FxcoJ166359098310502j1UGQOp_xw1sHnZf2TBLxIAVcI1pr_ptSG7GbI4Jh8JHPzpgXIVd6vHgcp4KUP7bIcL92ot4SobMNdIjsb6CeO0xXfdGg1DB166dh3n~lV6zvij0xVW8O87RwFvqyq8bfocRq2uG0yIAc6GJfPzG3Vt7W-bSkl68yzw3cggRUZpEKUJ0VpkW0x0Q0aGrCFLasnWujHANJMp2D1tUHzbtF-NKQkCBUiGE1ZKdTwYkeVoNQaOoU87ivURTKramyPzaIW67BRI6kPNkr3PLHsHc"};'
    ]

    p = []
    for i in range(len(cks)):
        p1 = Process(target=work, args=(killTime, cks[i], sku))
        p1.start()
        p.append(p1)

    for i in range(len(cks)):
        p[i].join()
