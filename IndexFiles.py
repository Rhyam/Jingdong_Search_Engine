INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def indexDocs(self, root, writer):   
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print("adding", filename)
                try:
                    path = os.path.join(root, filename)
                    file = open(path, encoding='gbk')
                    line = file.readlines()    #将文本中的内容逐行读出
                    name = line[0].strip()              #第一行为商品名称
                    imgurl = "https:" + line[1].strip()    #第二行为商品图片地址
                    current_price = line[2].strip()     #当前价格
                    refer_price = line[3].strip()       #参考价格
                    peak_price = line[4].strip()        #最高价格
                    url = line[5].strip()               #商品所在网页
                    order = url[20:32]                  #商品的序列
                    shop = line[6].strip()              #店铺名
                    label = line[7].strip()             #分层
                    logo_url = line[8].strip()          #logo
                    if logo_url != "NONE":
                        logo_url = "https:" + logo_url
                    shop_url = line[9].strip()          #店铺地址
                    if shop_url != "NONE":
                        shop_url = "https:" + shop_url
                    file.close()
                    
                    doc = Document()
                    doc.add(TextField("name", name, Field.Store.YES))
                    doc.add(TextField("imgurl", imgurl, Field.Store.YES))
                    doc.add(TextField('current_price', current_price, Field.Store.YES))
                    doc.add(TextField('refer_price', refer_price, Field.Store.YES))
                    doc.add(TextField('peak_price', peak_price, Field.Store.YES))
                    doc.add(TextField('url', url, Field.Store.YES))
                    doc.add(TextField('order', order, Field.Store.YES))
                    doc.add(TextField('shop', shop, Field.Store.YES))
                    doc.add(TextField('label', label, Field.Store.YES))
                    doc.add(TextField('logo_url', logo_url, Field.Store.YES))
                    doc.add(TextField('shop_url', shop_url, Field.Store.YES))
                    writer.addDocument(doc)
                except Exception as e:
                    print("Failed in indexDocs:", e)

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = StandardAnalyzer()
        IndexFiles('html', "index", analyzer)
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
