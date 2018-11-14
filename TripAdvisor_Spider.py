#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import requests
import time
import json
from bs4 import BeautifulSoup

class TripAdivsor():
    max_num = 99
    def __init__(self):
        self.temp_url = "https://www.tripadvisor.cn/Attractions-g60763-Activities-oa{}-New_York_City_New_York.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        }
        self.parse_times = 0

    # 请求相应URL,并返回HTML文档
    def parse_url(self, url):
        response = requests.get(url,headers=self.headers)
        # 请求前睡眠2秒
        time.sleep(2)
        if response.status_code != 200:
            print('parsing not success!--',url)
            # 请求不成功
            if self.parse_times < 3:
                # 重复请求三次
                self.parse_times += 1
                return self.parse_url(url)
            else:
                # 请求不成功, parse_times置为0
                self.parse_times = 0
                return None
        else:
            # 请求成功
            print('parsing success!--',url)
            # 请求成功, parse_times重置为0
            return response.text

    # 解析网页，并提取数据
    def parse_html(self, html):
        item_list = []
        # 使用BeautifulSoup解析网页
        soup = BeautifulSoup(html, 'lxml')
        # 提取网页中的最大页面数，病重置max_num
        if self.max_num == 99:
            # 小挑战：如何修改并获得其值
            max_num = soup.select("div.pageNumbers > a:nth-of-type(8)")
            print(max_num)
            self.max_num = self.max_num
        divs = soup.select("div.attraction_element")
        for div in divs:
            # 剔除干扰内容
            imgs = div.select("img[width='180']")[0]
            if imgs:
                title = div.select("div.listing_title > a")[0].get_text()
                # 格式化评论数，得到数字
                temp_comment = div.select("span.more > a")[0].get_text()
                comment = temp_comment.replace('\n', '').split("条")[0]
                # cate = div.select("div.p13n_reasoning_v2 > a > span")[0].get_text()
                cate = div.select("div.p13n_reasoning_v2")[0]
                cate_list = list(cate.stripped_strings)
                # 删除列表中无用的“，”，并生成一个规范的列表
                cate = list(filter(lambda x: x.replace(",", ''), cate_list))
                item = dict(
                    title=title,
                    comment=comment,
                    cate=cate,
                    )
                print(item)
                item_list.append(item)
            else:
                continue
        return item_list

    # 保存数据
    def save_item(self, item_list):
        with open('TripAdvisor.txt', 'a+', encoding='utf-8') as f:
            for item in item_list:
                json.dump(item, f, ensure_ascii=False, indent=2)
            f.close()
        print("Save success!")

    # 逻辑实现
    def run(self):
        # 1.Find URL
        for i in range(0, self.max_num):
            url = self.temp_url.format(i*30)
            # 2.Send Request, Get Response
            html = self.parse_url(url)
            # 3.Get item
            if html:
                item = self.parse_html(html)
                # 4.save information
                self.save_item(item)

if __name__=='__main__':
    spider = TripAdivsor()
    spider.run()

