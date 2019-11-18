# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    target = 'https://www.infoq.cn/article/graphite-intro'
    req = requests.get(url=target)
    html = req.text
    print(html)
#    bf = BeautifulSoup(html)
#    texts = bf.find_all('div', class_ = 'showtxt')
#    print(texts[0].text.replace('\xa0'*8,'\n\n'))