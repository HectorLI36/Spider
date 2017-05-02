# -*- coding:utf-8 -*-
"""
created on 2017-03-09
author: Hector Li
email: lihao.xjtu@hotmail.com
"""
from bs4 import BeautifulSoup
import urllib
import urllib2
import time
import numpy as np
import pymysql

ROOT_URL = 'http://www.imdb.com/title/tt4975722/reviews?start='
# http://www.imdb.com/title/tt4975722/reviews?start=0

# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]



def spider(page):
    text_list = []
    for i in range(10):
        time.sleep(np.random.rand() * 5)
        url = ROOT_URL + str(i * 10)
        req = urllib2.Request(url, headers=hds[i % len(hds)])
        source_code = urllib2.urlopen(req).read()
        plain_test = str(source_code)
        bs_obj = BeautifulSoup(plain_test)
        list_soup = bs_obj.find('div', {'id': 'tn15content'})
        comment_list = list_soup.findAll('p')
        for comment in comment_list:
            temp = comment.get_text()
            text_list.append(temp)
            try:
                conn = pymysql.connect()  # add your own db
                with conn.cursor() as cursor:
                    sql = r'INSERT INTO `my_test_db`.`moonlight_comments`(`comment`) VALUES(%s);'
                    rs_raw = cursor.execute(sql, temp)
                    conn.commit()
            except Exception, e:
                raise e
            print temp
        pass



spider(1)