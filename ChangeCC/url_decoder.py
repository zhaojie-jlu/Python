

import requests
from lxml import etree  # 导入库
from bs4 import BeautifulSoup
import re
import time


class Spider:
    # 定义爬虫类
    def __init__(self):
        self.url = 'https://movie.douban.com/cinema/nowplaying/beijing/'

        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }
        r = requests.get(self.url, headers=self.headers)
        r.encoding = r.apparent_encoding
        self.html = r.text

    def lxml_find(self):
        """用lxml解析"""
        start = time.time()  # 三种方式速度对比
        selector = etree.HTML(self.html)  # 转换为lxml解析的对象
        titles = selector.xpath('//li[@class="list-item"]/@data-title')  # 这里返回的是一个列表
        for each in titles:
            title = each.strip()  # 去掉字符左右的空格
            print(title)
        end = time.time()
        print('lxml耗时', end - start)

    def BeautifulSoup_find(self):
        """用BeautifulSoup解析"""
        start = time.time()
        soup = BeautifulSoup(self.html, 'lxml')  # 转换为BeautifulSoup的解析对象()里第二个参数为解析方式
        titles = soup.find_all('li', class_='list-item')
        for each in titles:
            title = each['data-title']
            print(title)
        end = time.time()
        print('BeautifulSoup耗时', end - start)

    def re_find(self):
        """用re解析"""
        start = time.time()
        titles = re.findall('data-title="(.+)"', self.html)
        for each in titles:
            print(each)
        end = time.time()
        print('re耗时', end - start)


if __name__ == '__main__':
    spider = Spider()
    spider.lxml_find()
    spider.BeautifulSoup_find()
    spider.re_find()
