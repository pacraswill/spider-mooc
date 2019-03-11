# coding=utf-8

import re
import requests
import traceback
from bs4 import BeautifulSoup


def getHTMLText(url, coding='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = coding
        return r.text
    except:
        return ''


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            #[0] 是为了去掉匹配不到的情况：匹配不到时返回空，对空取【0】会报错进入 except 继续循环
            lst.append(re.findall(r's[hz]\d{6}', i.attrs['href'])[0])
        except:
            continue


def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        html = getHTMLText(stockURL + stock + '.html')
        try:
            if not html:
                continue
            soup = BeautifulSoup(html, 'html.parser')
            infoDict = {}
            # find 得到的结果才能再调用find等函数， find_all不可以
            stockInfo = soup.find('div', attrs={'class': 'stock-info'})

            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                value = valueList[i].text
                infoDict[key] = value

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count += 1
                print('\r当前进度：{:.2f}%'.format(count * 100 / len(lst)), end='')
        except:
            count += 1
            print('\r当前进度：{:.2f}%'.format(count * 100 / len(lst)), end='')
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    stock_list = []
    output_file = '/Users/zhao/Desktop/stock.txt'
    getStockList(stock_list, stock_list_url)
    getStockInfo(stock_list, stock_info_url, output_file)


main()
