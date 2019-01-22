# -*- coding:utf-8 -*-
import time

import requests
import re
import urllib
import codecs

import sys

reload(sys)
sys.setdefaultencoding('UTF-8')
url = "https://m.weibo.cn/api/container/getIndex"
# 请求的url

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36",
}
# user-agent
ie7 = "User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"

ie8 = "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"

tt = "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"

agents = [ie7, ie8, tt]
params = {
    "type": "uid",
    "value": "{uid}",
    "containerid": "{containerid}",
    "page": "{page}"}


# 请求携带的参数


def get_data(uid="3303658163", containerid="1005053303658163"):
    try_time = 0
    total = 3000  # 打算爬取的页数，比如100页
    content = []  # 存放获取到的微博正文内容
    page = 1  # 页码，从第一页开始算
    last_length = -1  # 上一个的内容长度，用于对比上一次的总体内容长度跟这次是否一致，如果一致，则认为没有新数据，停止脚本处理
    for i in range(total):
        params["page"] = str(page)
        params['value'] = uid
        params['containerid'] = str(containerid)
        res = requests.get(url, headers=headers, params=params)
        # 如果接口返回不为空才返回下一步
        if res.content != "":
            print(res.json().get("data"))
            cards = res.json().get("data").get("cards")
            # 获取carads下的所有项
            for card in cards:
                if card.get("card_type") == 9:
                    text = card.get("mblog").get("text")
                    kw = urllib.quote(text.encode('UTF-8'))
                    old_kw = re.sub("%0A", "", kw)
                    new_text = urllib.unquote(old_kw)
                    # %0A  这串数字对应的就是这个回车字符python try catch
                    pattern = re.compile(r"<.*?>|转发微博|查看图片|查看动图|&gt;")
                    # 这里就是把<>符号内的都匹配出来,正则规则
                    text = re.sub(pattern, "", new_text)
                    content.append(text)
        if len(content) == last_length:
            if try_time >= 3:
                print("已经获取不到更多内容，脚本暂停处理")
                break
            time.sleep(5)
            try_time += 1
            # 替换新的 浏览器标识
            headers['User-Agent'] = agents.pop(0)
            agents.append(headers['User-Agent'])
            print ("正在尝试重新获取")

        else:
            # 每次成功抓取内容充值重试次数
            try_time = 0
            last_length = len(content)
            print("抓取第{page}页，目前总共抓取了 {count} 条微博".format(page=page, count=len(content)))
            with codecs.open('jb.txt', 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
            page += 1


if __name__ == '__main__':
    get_data("1739928273", "1076031739928273")
