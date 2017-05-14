# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import re
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


class Pre_CS_bitch():
    def __init__(self):
        # self.url = 'http://www.newxue.com/xxsx/'
        self.headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.big_title_list = []

    def first_page(self,url):
        html = requests.get(url,headers=self.headers).content
        html = html.decode('gb2312').encode('utf-8')
        soup_one = BeautifulSoup(html,"html.parser")
        big_title = soup_one.find_all('p')
        for i in big_title[:-1]:
            self.big_title_list.append(i.text)
        # print self.big_title_list
        content = re.compile(r'<p class="ywxfl">(.*?)</ul>',re.S)
        big_content = re.findall(content,html)
        for j in big_content:
            t_firstpage = r'(.*?)</p>'
            title_firstpage = re.findall(t_firstpage,j)# 每本书的每一章节标题
            # print title_firstpage[0]
            con_firstpage = re.compile(r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>',re.S)
            content_firstpage = re.findall(con_firstpage,j)
            for item in content_firstpage:
                # print item[0],item[1]
                ## 创建层级目录
                os.makedirs(r'D:/python_spider/bitch/chinese/%s/%s'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8')))

##-------封装模块，以便以后调用---------##
if __name__ == '__main__':
    mvp = Pre_CS_bitch().first_page('http://www.newxue.com/yuwen/rjkb1a/')

