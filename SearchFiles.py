#519030910026 黄榕基 SearchFiles

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import search_by_CNN as cnn

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

def search_relevancy(searcher, analyzer, keyword, opt):
    if opt == 1:
        query = QueryParser("name", analyzer).parse(keyword)
    elif opt == 2:    
        query = QueryParser("label", analyzer).parse(keyword)
    scoreDocs = searcher.search(query, 50).scoreDocs

    result_list = []
    brand_list = []
    label_list = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        result  =  {"name" : doc.get("name"), \
                    "imgurl" : doc.get("imgurl"), \
                    "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                    "refer_price" : doc.get("refer_price"), \
                    "peak_price" : doc.get("peak_price"), \
                    "url" : doc.get("url"), \
                    "shop" : doc.get("shop"), \
                    "label" : '>>'.join(doc.get("label").split()), \
                    "logo_url" : doc.get("logo_url"), \
                    "shop_url" : doc.get("shop_url")}
        result_list.append(result)
        if doc.get("shop") not in brand_list and len(brand_list) < 5:
            brand_list.append(doc.get("shop"))
        if doc.get("label").split()[2] not in label_list and len(label_list) < 5:
            label_list.append(doc.get("label").split()[2])

    for i in range(5 - len(brand_list)):
        brand_list.append('')
    for i in range(5 - len(label_list)):
        label_list.append('')

    return result_list, brand_list, label_list

def search_price(searcher, analyzer, keyword, opt):
    if opt == 1:
        query = QueryParser("name", analyzer).parse(keyword)
    elif opt == 2:
        query = QueryParser("label", analyzer).parse(keyword)
    scoreDocs = searcher.search(query, 100).scoreDocs

    prices = {}
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        order = doc.get("order")
        current_price = doc.get("current_price")
        if current_price != '-1.00':
            prices[order] = float(current_price)
        if len(prices) == 50:
            break

    prices = sorted(prices.items(), key=lambda x: x[1])
    result_list = []
    brand_list = []
    label_list = []
    for order, current_price in prices:
        query = QueryParser("order", analyzer).parse(order)
        scoreDocs = searcher.search(query, 1).scoreDocs
        doc = searcher.doc(scoreDocs[0].doc)
        result  =  {"name" : doc.get("name"), \
                    "imgurl" : doc.get("imgurl"), \
                    "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                    "refer_price" : doc.get("refer_price"), \
                    "peak_price" : doc.get("peak_price"), \
                    "url" : doc.get("url"), \
                    "order" : doc.get("order"), \
                    "shop" : doc.get("shop"), \
                    "label" : '>>'.join(doc.get("label").split()), \
                    "logo_url" : doc.get("logo_url"), \
                    "shop_url" : doc.get("shop_url")}
        result_list.append(result)
        if doc.get("shop") not in brand_list and len(brand_list) < 5:
            brand_list.append(doc.get("shop"))
        if doc.get("label").split()[2] not in label_list and len(label_list) < 5:
            label_list.append(doc.get("label").split()[2])

    for i in range(5 - len(brand_list)):
        brand_list.append('')
    for i in range(5 - len(label_list)):
        label_list.append('')
        
    return result_list, brand_list, label_list

def shopsearch(searcher, analyzer, keyword):
    result_list = []
    query = QueryParser("shop", analyzer).parse(keyword)
    scoreDocs = searcher.search(query, 100).scoreDocs
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if keyword not in doc.get("shop"):
            continue
        else:
            result  =  {"name" : doc.get("name"), \
                        "imgurl" : doc.get("imgurl"), \
                        "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                        "refer_price" : doc.get("refer_price"), \
                        "peak_price" : doc.get("peak_price"), \
                        "url" : doc.get("url"), \
                        "shop" : doc.get("shop"), \
                        "label" : '>>'.join(doc.get("label").split()), \
                        "logo_url" : doc.get("logo_url"), \
                        "shop_url" : doc.get("shop_url")}
            result_list.append(result)
        if len(result_list) == 50:
            break

    return result_list

def imgsearch(searcher, analyzer, keyword):
    order_list = cnn.imgorder(keyword)
    
    result_list = []
    for order, differ in order_list:
        query = QueryParser("order", analyzer).parse(order)
        scoreDocs = searcher.search(query, 1).scoreDocs
        doc = searcher.doc(scoreDocs[0].doc)
        if len(result_list) == 0:
            certain_label = doc.get("label").split()
        flag = False
        if doc.get("label").split()[2] == certain_label[2]:
            flag = True

        if flag == True:
            result  =  {"name" : doc.get("name"), \
                        "imgurl" : doc.get("imgurl"), \
                        "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                        "refer_price" : doc.get("refer_price"), \
                        "peak_price" : doc.get("peak_price"), \
                        "url" : doc.get("url"), \
                        "order" : doc.get("order"), \
                        "shop" : doc.get("shop"), \
                        "label" : '>>'.join(doc.get("label").split()), \
                        "logo_url" : doc.get("logo_url"), \
                        "shop_url" : doc.get("shop_url")}
            result_list.append(result)

        if len(result_list) == 10:
            break

    return result_list

def logosearch(searcher, analyzer, keyword):
    shop = cnn.logo_shop(keyword)
    query = QueryParser("shop", analyzer).parse(shop)
    scoreDocs = searcher.search(query, 50).scoreDocs
    result_list = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if doc.get("shop") != shop:
            break
        result  =  {"name" : doc.get("name"), \
                    "imgurl" : doc.get("imgurl"), \
                    "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                    "refer_price" : doc.get("refer_price"), \
                    "peak_price" : doc.get("peak_price"), \
                    "url" : doc.get("url"), \
                    "order" : doc.get("order"), \
                    "shop" : doc.get("shop"), \
                    "label" : '>>'.join(doc.get("label").split()), \
                    "logo_url" : doc.get("logo_url"), \
                    "shop_url" : doc.get("shop_url")}
        result_list.append(result)
    return result_list

def filt_search(searcher, analyzer, keyword, opt, filt, limit):
    if opt == 1:
        query = QueryParser("name", analyzer).parse(keyword)
    elif opt == 2:    
        query = QueryParser("label", analyzer).parse(keyword)
    scoreDocs = searcher.search(query, 1000).scoreDocs

    result_list = []
    brand_list = []
    label_list = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        result  =  {"name" : doc.get("name"), \
                    "imgurl" : doc.get("imgurl"), \
                    "current_price" : '已下架' if doc.get("current_price") == '-1.00' else doc.get("current_price"), \
                    "refer_price" : doc.get("refer_price"), \
                    "peak_price" : doc.get("peak_price"), \
                    "url" : doc.get("url"), \
                    "shop" : doc.get("shop"), \
                    "label" : '>>'.join(doc.get("label").split()), \
                    "logo_url" : doc.get("logo_url"), \
                    "shop_url" : doc.get("shop_url")}
        if filt == 0:
            if doc.get("shop") == limit:
                result_list.append(result)
                if doc.get("shop") not in brand_list and len(brand_list) < 5:
                    brand_list.append(doc.get("shop"))
                if doc.get("label").split()[2] not in label_list and len(label_list) < 5:
                    label_list.append(doc.get("label").split()[2])
        if filt == 1:
            if doc.get("label").split()[2] == limit:
                result_list.append(result)
                if doc.get("shop") not in brand_list and len(brand_list) < 5:
                    brand_list.append(doc.get("shop"))
                if doc.get("label").split()[2] not in label_list and len(label_list) < 5:
                    label_list.append(doc.get("label").split()[2])
        if len(result_list) == 50:
            break
    
    for i in range(5 - len(brand_list)):
        brand_list.append('')
    for i in range(5 - len(label_list)):
        label_list.append('')
    
    return result_list, brand_list, label_list

def work(keyword, vm_env, opt, sort=None, filt=None, limit=None):       #keyword关键词，opt为1按名字搜索、2按标签搜索、3按图片搜索、4按Logo搜索，sort为0按相关度排序、1按价格排序
    if keyword == '':
        return
    if sort == None:
        sort = 0

    STORE_DIR = "index"
    vm_env.attachCurrentThread()
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    if filt != None:
        result_list, brand_list, label_list = filt_search(searcher, analyzer, keyword, opt, filt, limit)
    else:
        if sort == 0:
            if opt == 3:
                result_list = imgsearch(searcher, analyzer, keyword)
                brand_list = None
                label_list = None
            elif opt == 4:
                result_list = logosearch(searcher, analyzer, keyword)
                brand_list = None
                label_list = None
            elif opt == 5:
                result_list = shopsearch(searcher, analyzer, keyword)
                brand_list = None
                label_list = None
            else:
                result_list, brand_list, label_list = search_relevancy(searcher, analyzer, keyword, opt)
        if sort == 1:
            result_list, brand_list, label_list = search_price(searcher, analyzer, keyword, opt)
    del searcher
    return result_list, brand_list, label_list
"""
if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    keyword = input("请输入要搜索的图片的名字：")
    print(search_relevancy(searcher, analyzer, keyword, 2))
    del searcher
"""