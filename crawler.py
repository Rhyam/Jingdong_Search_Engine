import json
import os
import sys
import time
import random
import string
import threading

import pymysql
import requests
from lxml import etree

def valid_filename(s):              #将网站名转化为合法的文件名
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    s = s[0:255]
    return s + '.txt'

def add_page_to_folder(goods_name, good_web_page,good_photo,good_price_now,good_price_order,good_price_top,shop_name,good_tag,shop_logo,shop_web_page):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(good_web_page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(str(good_web_page.encode('ascii', 'ignore')) + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    try:
        f = open(os.path.join(folder, filename), 'w')
        f.write((goods_name + \
                '\n' + good_photo + \
                '\n' + good_price_now + \
                '\n' + good_price_order + \
                '\n' + good_price_top + \
                '\n' + good_web_page + \
                '\n' + shop_name + \
                '\n' + good_tag + \
                '\n' + shop_logo + \
                '\n' + shop_web_page))  # 将所爬取到的商品结构化信息存入文件
        f.close()
    except:
        pass

def url_complete(host, url):
    '''
    补充网址
    '''
    if 'http' not in url:
        return host + url
    return url

def request(header, method, url):
    '''
    外层包装的request函数
    '''
    if method == 'get':
        r=requests.get(url,headers=header)
    elif method == 'post':
        r=requests.post(url,headers=header)
    r.encoding = 'utf-8'
    tree = etree.HTML(r.text)
    return tree, r

UserAgent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        ]                       #每次发送请求随计选择一个useragent，防止一个useragent大量访问被服务器拒绝

headers = { 'User-Agent': '',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'}
url_token_list = []
web_page_count = 0

def _get_goods_information_(k):                             #爬虫的主程序
    for i in range(100008016560+k,100008400000):            #通过循环控制商品id
        try:
            time.sleep(1)                                                       #每次访问间隔1秒中，体现爬虫的礼貌性
            page = "https://item.jd.com/{}.html".format(i)                      #商品的网站url
            headers['User-Agent'] = random.choice(UserAgent_list)
            tree,response = request(header=headers,method='get',url=page)       #向服务器发送请求

            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            goods_names = tree.xpath("//div[@class='sku-name']/text()")
            if len(goods_names) == 2:
                goods_name = goods_names[1].strip()
                print(goods_name)
            if len(goods_names) == 1:
                goods_name = goods_names[0].strip()
                print(goods_name)
            #print(tree.xpath("//div[@class='sku-name']/text()"))

            good_photo = tree.xpath("//img[@id='spec-img']/@data-origin")[0]
            print(good_photo)

            #good_price = tree.xpath("//strong[@class='J-p-{}']/text()".format(i))
            page_price = "http://p.3.cn/prices/mgets?skuIds=J_" + str(i)
            headers['User-Agent'] = random.choice(UserAgent_list)
            tree0,response0 = request(header=headers,method='get',url=page_price)
            good_price_now = response0.json()[0]['p']                                   #商品当前价格
            good_price_top = response0.json()[0]['m']                                   #商品最高价
            good_price_order = response0.json()[0]['op']                                #商品指导价
            
            good_web_page = page
            print(good_web_page)

            shop_name = tree.xpath("//a[@clstag='shangpin|keycount|product|mbNav-5']/text()")[0]
            print(shop_name)

            good_tag = tree.xpath("//a[@clstag='shangpin|keycount|product|mbNav-1']/text()")[0]
            good_tag = good_tag + ' ' + tree.xpath("//a[@clstag='shangpin|keycount|product|mbNav-2']/text()")[0]
            good_tag = good_tag + ' ' + tree.xpath("//a[@clstag='shangpin|keycount|product|mbNav-3']/text()")[0]
            print(good_tag)

            try:
                shop_logo = tree.xpath("//div[@class='shop-logo-box']/a/img/@src")[0]
            except:
                try:
                    shop_logo = tree.xpath("//div[@class='J_ShopSignImg d-img-wrap']/img/@src")[0]
                except:
                    shop_logo = 'NONE'
            print(shop_logo)


            try:
                shop_web_page = tree.xpath("//div[@class='name']/a/@href")[0]
            except:
                shop_web_page = "NONE"
            print(shop_web_page)

            add_page_to_folder(goods_name, good_web_page,good_photo,good_price_now,good_price_order,good_price_top,shop_name,good_tag,shop_logo,shop_web_page)
            i = i + 10
        except:
            i = i + 10
            continue
        print("-------------------------------------------------------")


def _main_():
    threading_num = int(input('请输入需要的线程数量'))
    for k in range(threading_num):          #建立多个线程并开始工作
        t = threading.Thread(target=_get_goods_information_(k),args=())
        t.setDaemon(True)
        t.setName(str(k))
        t.start

_main_()