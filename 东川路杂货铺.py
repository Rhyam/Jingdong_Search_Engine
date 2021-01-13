import sys, os, lucene
from java.io import File
import numpy as np
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
import SearchFiles as search   #引入SearchFiles中的函数
#import imSearchFiles as imsearch   #引入SearchFiles中的函数
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
"""
以下分别设置了四个路由分别为网页搜索的输入页面、结果页面以及图片搜索的输入页面、结果页面
四个网页的路由分别为'/' '/ressult' '/im' '/imresult'
"""
#路由1,商品名称网页
@app.route('/', methods=['POST', 'GET'])
def name_form():
    if request.method == "POST":                  #post 请求让用户输入查询关键词
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword))     
    return render_template("商品名称搜索.html")

@app.route('/naresult', methods=['POST','GET'])
def naresult():
    keyword = request.args.get('keyword')              #获取用户输入的关键词
    f=open("temp_file","w")
    f.write(keyword)
    f.close()  
    search_list_1,list_2,list_3=search.work(keyword,vm_env,1,None,None,None)       #获得返回的列表
    np.save("file1.npy",list_2)
    np.save("file2.npy",list_3)
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)   #将keyword和字符列表传入html表单

@app.route('/mat_naresult',methods=['POST','GET'])
def mat_naresult():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list_2,list_3=search.work(keyword,vm_env,1,None,None,None)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/pri_naresult',methods=['POST','GET'])
def pri_naresult():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list_2,list_3=search.work(keyword,vm_env,1,1,None,None)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

#路由2，商品标签网页
@app.route('/la', methods=['POST', 'GET'])
def lable_form():
    if request.method == "POST":                  #post 请求让用户输入查询关键词
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword))     
    return render_template("商品标签搜索.html") 

@app.route('/laresult', methods=['POST','GET'])
def laresult():
    keyword = request.args.get('keyword')              #获取用户输入的关键词
    f=open("temp_file","w")
    f.write(keyword)
    f.close()
    search_list_2,list_2,list_3= search.work(keyword,vm_env,2,None,None,None)       #获得返回的列表
    np.save("file1.npy",list_2)
    np.save("file2.npy",list_3)
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3)   #将keyword和字符列表传入html表单

@app.route('/mat_laresult',methods=['POST','GET'])
def mat_laresult():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,None,None)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/pri_laresult',methods=['POST','GET'])
def pri_laresult():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,1,None,None)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 



#路由3，商品图片网页
@app.route('/im', methods=['POST', 'GET'])
def image_form():
    return render_template('商品图片搜索.html')

@app.route('/imresult', methods=['POST', 'GET'])
def imresult():
    img = request.files.get('file')
    img.save(os.path.join('image', "1.jpg"))
    search_list_3,list2,list3= search.work("1",vm_env,3,None,None,None)
    return render_template("商品图片结果.html",keyword="yes",search_list_3=search_list_3)

#路由4，商品logo网页
@app.route('/lo', methods=['POST', 'GET'])
def logo_form():
    return render_template('商品logo搜索.html')

@app.route('/loresult', methods=['POST', 'GET'])
def loresult():
    img = request.files.get('file')
    img.save(os.path.join('image', "1.jpg"))
    search_list_4,list2,list3= search.work("1",vm_env,4,None,None,None)
    return render_template("商品logo结果.html",keyword="yes",search_list_4=search_list_4)

#路由5，商品店铺网页
@app.route('/sh', methods=['POST', 'GET'])
def shop_form():
    if request.method == "POST":                  #post 请求让用户输入查询关键词
        keyword=request.form['keyword']                        
        return redirect(url_for('shresult', keyword=keyword))     
    return render_template("商品店铺搜索.html")

@app.route('/shresult', methods=['POST','GET'])
def shresult():
    keyword = request.args.get('keyword')              #获取用户输入的关键词
    f=open("temp_file","w")
    f.write(keyword)
    f.close()
    search_list_5,list_2,list_3= search.work(keyword,vm_env,5,None,None,None)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('shresult', keyword=keyword)) 
    return render_template("商品店铺结果.html", keyword=keyword, search_list_5=search_list_5,list_2=list_2,list_3=list_3)
#对于商品名称搜索的10个button按钮
@app.route('/naresult1',methods=['POST','GET'])
def naresult1():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,0,list_2[0])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult2',methods=['POST','GET'])
def naresult2():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,0,list_2[1])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult3',methods=['POST','GET'])
def naresult3():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,0,list_2[2])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult4',methods=['POST','GET'])
def naresult4():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,0,list_2[3])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult5',methods=['POST','GET'])
def naresult5():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,0,list_2[4])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult6',methods=['POST','GET'])
def naresult6():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,1,list_3[0])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult7',methods=['POST','GET'])
def naresult7():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,1,list_3[1])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)
    
@app.route('/naresult8',methods=['POST','GET'])
def naresult8():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,1,list_3[2])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult9',methods=['POST','GET'])
def naresult9():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,1,list_3[3])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

@app.route('/naresult10',methods=['POST','GET'])
def naresult10():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy")
    list_3=np.load("file2.npy")
    search_list_1,list2,list3=search.work(keyword,vm_env,1,None,1,list_3[4])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('naresult', keyword=keyword)) 
    return render_template("商品名称结果.html", keyword=keyword, search_list_1=search_list_1,list_2=list_2,list_3=list_3)

#另外10个button
@app.route('/laresult1', methods=['POST','GET'])
def laresult1():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,0,list_2[0])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult2', methods=['POST','GET'])
def laresult2():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,0,list_2[1])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult3', methods=['POST','GET'])
def laresult3():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,0,list_2[2])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult4', methods=['POST','GET'])
def laresult4():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,0,list_2[3])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult5', methods=['POST','GET'])
def laresult5():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,0,list_2[4])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult6', methods=['POST','GET'])
def laresult6():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,1,list_3[0])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult7', methods=['POST','GET'])
def laresult7():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,1,list_3[1])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult8', methods=['POST','GET'])
def laresult8():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,1,list_3[2])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult9', methods=['POST','GET'])
def laresult9():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,1,list_3[3])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

@app.route('/laresult10', methods=['POST','GET'])
def laresult10():
    f=open("temp_file",'r')
    keyword=f.read()
    f.close()
    list_2=np.load("file1.npy",allow_pickle=True)
    list_3=np.load("file2.npy",allow_pickle=True)
    search_list_2,list2,list3=search.work(keyword,vm_env,2,None,1,list_3[4])       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('laresult', keyword=keyword)) 
    return render_template("商品标签结果.html", keyword=keyword, search_list_2=search_list_2,list_2=list_2,list_3=list_3) 

"""
#路由3, 商品图片网页
@app.route('/im', methods=['POST', 'GET'])
def image_form():
    if request.method == "POST":                  #post 请求让用户输入查询关键词
        img=request.file.get['file']                        
        return redirect(url_for('imresult', keyword=keyword))     
    return render_template("商品图片搜索.html") 
    
@app.route('/imresult', methods=['POST','GET'])
def imresult():
    keyword = request.file.get('keyword')              #获取用户输入的关键词
    search_list_3= imsearch.search_for_key(keyword,vm_env)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('imresult', keyword=keyword)) 
    return render_template("商品图片结果.html", keyword=keyword, search_list_3=search_list_3)
"""
"""
#路由4，关键词网页
@app.route('/ke', methods=['POST', 'GET'])
def key_form():
    if request.method == "POST":                  #post 请求让用户输入查询关键词
        keyword=request.form['keyword']                        
        return redirect(url_for('keresult', keyword=keyword))     
    return render_template("关键词搜索.html") 

@app.route('/keresult', methods=['POST','GET'])
def keresult():
    keyword = request.args.get('keyword')              #获取用户输入的关键词
    search_list_2= imsearch.search_for_key(keyword,vm_env)       #获得返回的列表
    if request.method == "POST":
        keyword=request.form['keyword']                        
        return redirect(url_for('keresult', keyword=keyword)) 
    return render_template("关键词结果.html", keyword=keyword, search_list_2=search_list_2)

"""


"""
以下三个函数为自定义的filter，用于在获取字符串列表不同位置的内容
"""

def pos1(li):
    return li[0]

def pos2(li):
    return li[1]

def pos3(li):
    return li[2]

def pos4(li):
    return li[3]

def pos5(li):
    return li[4]

def one(dic):
    return dic["name"]

def two(dic):
    return dic["imgurl"]

def three(dic):
    return dic["current_price"]

def four(dic):
    return dic["refer_price"]

def five(dic):
    return dic["peak_price"]

def six(dic):
    return dic["url"]

def seven(dic):
    return dic["shop"]

def eight(dic):
    return dic["label"]

def nine(dic):
    return dic["logo_url"]

def ten(dic):
    return dic["shop_url"]

if __name__ == '__main__':
    vm_env=lucene.initVM(vmargs=['-Djava.awt.headless=true'])      #初始化lucene线程
    app.add_template_filter(pos1,'pos1')
    app.add_template_filter(pos2,'pos2')
    app.add_template_filter(pos3,'pos3')
    app.add_template_filter(pos4,'pos4')
    app.add_template_filter(pos5,'pos5')
    app.add_template_filter(one,'one')
    app.add_template_filter(two,'two')
    app.add_template_filter(three,'three')
    app.add_template_filter(four,'four')
    app.add_template_filter(five,'five')
    app.add_template_filter(six,'six')
    app.add_template_filter(seven,'seven')
    app.add_template_filter(eight,'eight')
    app.add_template_filter(nine,'nine')
    app.add_template_filter(ten,'ten')
    app.run(debug=True, port=8081)        #运行程序