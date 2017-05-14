# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import time
import random
import urllib

import pre_bitch

reload(sys)
sys.setdefaultencoding('utf-8')

class CS_bitch():
    def __init__(self):
        self.url = 'http://www.newxue.com/czsx/'
        self.headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.big_title_list = []
        # self.mvp = pre_bitch.Pre_CS_bitch().first_page('self.url')

    def first_page(self):
        pre_bitch.Pre_CS_bitch().first_page(self.url) # 导入创建好的目录
        html = requests.get(self.url,headers=self.headers).content
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
                # os.makedirs(r'D:/python_spider/bitch/%s/%s'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8')))
                try:
                    html_sec = requests.get('%s'%item[0],headers=self.headers).content
                    html_sec = html_sec.decode('gbk').encode('utf-8')
                    kw_dst = re.compile(r'<div id="kw_dst"><ul>.*?<li>(.*?)</ul></div>',re.S)
                    kw_home = re.findall(kw_dst,html_sec)
                except UnicodeDecodeError:
                    continue
                for link in kw_home:
                    sub = r'<li><a href="(.*?)" target="_blank"><div class="kkk"><span class="kwml_left">(.*?)</span><span class="kwml_rit">'
                    sub_link = re.findall(sub,link)
                    for mm in sub_link:
                        # print mm[0],mm[1] # 最后的连接和标题
                        try:
                            sub_html = requests.get('%s'%mm[0],headers=self.headers).content
                            sub_html = sub_html.decode('gbk').encode('utf-8')
                            # print sub_html
                            mmmm = re.compile(r'<div class="jclj_bt"><h1>(.*?)</h1></div>.*?<div class="jclj_text">(.*?)</p></div>',re.S)
                            mm_title_content = re.findall(mmmm,sub_html)
                            try:
                                mm_title_content_text = mm_title_content[0][1]
                                if mm_title_content_text:
                                    cc = r'src="(.*?)"'
                                    cc_get = re.findall(cc,mm_title_content_text)
                                    for pp in cc_get:
                                        try:
                                        # print pp
                                            url = 'http://www.newxue.com/'+ pp
                                            # path_root = 'D:/python_spider/bitch/student/picture/'
                                            pp = pp.split('/')
                                            pp = '%s_%s_%s'%(pp[-3],pp[-2],pp[-1])
                                            # path_add = '%s.jpg'% pp
                                            path = 'D:/python_spider/bitch/student/picture/%s.jpg'%pp
                                            urllib.urlretrieve(url,path)
                                        except IOError:
                                            continue
                                #将文章变成正常人看的模式
                                # mm_title_content_text = mm_title_content[0][1].replace('<p>','\n').replace('<strong>','--')
                                # mm_title_content_text = mm_title_content_text.replace('</p>','').replace('</strong>','--')
                                # p = re.compile(r'<[^>]+>')
                                # mm_title_content_text = re.sub(p,'',mm_title_content_text)
                                print mm_title_content[0][0]
                            except IndexError:
                                continue
                        except UnicodeDecodeError:
                            continue
                        # a = os.makedirs(r'D:/python_spider/bitch/%s/%s/%s.txt'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8'),mm_title_content[0][0].decode('utf-8')))
                        # with open(a,'wb') as f:
                        #     f.write(mm_title_content[0][1])
                        # a = os.getcwd()
                        # f = open('%s/%s'%(os.makedirs(r'D:/python_spider/bitch/%s/%s/'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8'))),mm_title_content[0][0].decode('utf-8'))+'.txt','r')
                        # f.write(mm_title_content[0][1])

                        root = 'D:/python_spider/bitch/chinese/'
                        root_one = '%s'%title_firstpage[0].decode("utf-8")
                        root_two = '%s'% item[1].decode("utf-8")
                        root_three = '%s'% mm_title_content[0][0].decode("utf-8") +'.txt'
                        root_tot = root + root_one +'/'+ root_two +'/'+ root_three
                        # print root_tot
                        f = open(root_tot,'w')
                        f.write('||||%s||||\n'% item[0])
                        f.write('%s||||\n'%title_firstpage[0].decode("utf-8"))
                        f.write('人教版||||\n')
                        f.write('%s||||\n'%item[1].decode("utf-8"))
                        f.write('%s  %s####\n'%(title_firstpage[0].decode("utf-8"),mm_title_content[0][0].decode("utf-8")))
                        f.write('%s####\n\n\n'%mm[0].decode("utf-8"))
                        f.write('%s\n\n'%mm_title_content_text)
                        f.write('%s,%s,%s\n'%(title_firstpage[0].decode("utf-8"),item[1].decode("utf-8"),mm_title_content[0][0].decode("utf-8")))
                        # os.makedirs(r'D:/python_spider/bitch/%s/%s/'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8')))
                        # a = os.getcwd()
                        # print a
                        # with open(mm_title_content[0][0].decode('utf-8')+'.txt','w') as f:
                        #     f.write(mm_title_content[0][1])
            print u'%s完成'% title_firstpage[0].decode("utf-8")
            time.sleep(random.uniform(2.0,10.0))

                        # os.makedirs(r'D:/python_spider/bitch/%s/%s/'%(title_firstpage[0].decode('utf-8'),item[1].decode('utf-8')))


a = CS_bitch().first_page()
