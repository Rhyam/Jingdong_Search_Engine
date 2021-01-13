# Jingdong_Search_Engine
## need to open in **Docker**

### crawler.py
爬虫程序，爬取京东商品信息，每个商品存为一个html文件于html文件夹下

### 东川路杂货铺.py
网站的运行程序，在docker中运行该文件即可打开网页

### templates
该文件夹存放了包括商品名称搜索，商品标签搜索，商品图片搜索，商品店铺搜索，商品logo搜索的10个html前端文件

### image
暂存一张图片(image/1.jpg)，为用过上传的用于检索的图片

### temp_file
暂存一个关键词，为用户输入的文本内容

### file1.npy & file2.npy
各暂存一个列表，为用于过滤的商品品牌列表和商品标签列表

### static
静态文件夹，存放网页背景图

### img_pre.py
下载爬虫爬取的商品的图片和logo图片并用Resnet50通过CNN算法计算出特征向量，同时计算哈希存入二进制文件中
#### dataset/img_hash_in_Docker.npy & logo_hash_in_Docker.npy
存储图片与logo的哈希值的二进制文件

### IndexFiles.py
对html中的txt文件逐个处理，将商品的信息分类建立索引
#### index
索引文件夹

### SearchFiles.py
搜索函数，实现各种搜索，被 东川路杂货铺.py 调用

### search_by_CNN
实现图片搜索和logo搜索的函数，被SearchFiles.py调用

### img_search_test
存放两张测试用图片，分别用于图片搜索和Logo搜索
