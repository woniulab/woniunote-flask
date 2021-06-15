# 通过死循环加时间判断的方式来执行定时任务
import os, glob, requests
import time

while True:
    now = time.strftime('%H:%M')
    if now == '02:00':
        # 每天清空index-static缓存目录文件
        list = glob.glob('../template/index-static/*.html')
        for file in list:
            os.remove(file)
        # 清空完成后，再调用http://127.0.0.1:5000/static重新生成
        requests.get('http://127.0.0.1:5000/static')
        print('%s: 成功清空缓存文件并重新生成.' % now)
    time.sleep(60)  # 暂时时间不能低于60秒，也不能多于120秒
