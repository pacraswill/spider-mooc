# coding=utf-8

import requests
import re


'''
此实战项目重点在于：
1、在请求时需要添加 cookie  （不需要登陆淘宝）
2、翻页 url 的规律找寻
另外，淘宝搜索第一页有48个商品，之后是44个商品
'''


def getHTMLText(url):
    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        cookie = 'cna=mjpfFAacN3kCAXL3ONg5wK2P; miid=334963751200535338; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _cc_=WqG3DMC9EA%3D%3D; tg=0; enc=CCW9T3VfMCeLyO%2FDKvh6zd8h8K96FYq%2FkA%2Br5WDjr6jGlXSlZLzJbXaTYwycmwWs5ElCPbocUbANqAGAVoUbyQ%3D%3D; t=89aa6dcb125219f4ee839cd0a0ccfdf3; l=bBgg1XFPvJXaPqYGBOCZquI8Lrb9SIRYXuPRwCDXi_5Bf_T6_j7OloRNbE962j5R_CTB4R3ZAF99-etXj; _m_h5_tk=c89a5ffbf1d1f04f3097d95140dfbdf8_1551704692448; _m_h5_tk_enc=8587237f17bad35f5ff918b109ddeda6; cookie2=5292e1fa89f082f2a56bf5ab73c75cbe; _tb_token_=7e8e1f43367ae; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; mt=ci=0_0; v=0; JSESSIONID=6BE0F7D8ECD785A9E6864697EFE17EC6; isg=BOHh3azBGc_Yy7Ic_ri817Dh8Ks7Jlbp8vS9p0O23ehHqgF8i95lUA_qDJ6JYu24'
        headers = {'user-agent': user_agent, 'cookie': cookie}
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.url)
        print(url, r.status_code)
        return r.text
    except:
        return ''


def parsepage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]+\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print('失败')


def printGoodsList(ilt):
    tplt = '{:4}\t{:8}\t{:16}'
    print(tplt.format('序号', '价格', '商品名称'))
    count = 0

    for g in ilt:
        count += 1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = '耳机'
    depth = 2
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsepage(infoList, html)
        except:
            continue
    printGoodsList(infoList)


main()
