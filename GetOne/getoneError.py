# -*- coding: utf-8 -*-

#from "http://wufazhuce.com/one/vol.num"

import urllib2
import urllib
import time
import gzip
#import chardet
import json

import thread
from StringIO import StringIO
from bs4 import BeautifulSoup


#show now path
import os
homedir = os.getcwd()
print("now you are at "+homedir)

#可调整的参数
isdebug=True;
threadsize = 100 #同时处理页面数
oldlistcheck = 5 #出错判定阈值

print_lock = thread.allocate_lock()
list_lock = thread.allocate_lock()
leftlist = []

def saveImage(filename,addr):
    with open(filename, 'wb') as f:
        f.write(urllib.urlopen(addr).read())
def handle_response(resultdata):
    if resultdata.info().get('Content-Encoding') == 'gzip' :
        buf = StringIO(resultdata.read())
        f = gzip.GzipFile(fileobj = buf)
        ret = f.read()
    else:
        ret = resultdata.read()
    #print chardet.detect(ret)
    #print ret.decode("utf-8")
    return ret
def handle_text(origintest):
    return " ".join(origintest.split())

#处理 序号为pageindex的页面
def getdetail(pageindex):
    global leftlist
    global isdebug
    host="http://wufazhuce.com"
    if isdebug:
        #访问信息
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)

    #################图片#################
    # /one/1200
    myUrl = host+"/one/"+str(pageindex)
    result = urllib2.urlopen(urllib2.Request(myUrl))
    data = handle_response(result)
    soup = BeautifulSoup(data,'lxml')#soup = BeautifulSoup(data)
    #print soup.prettify()

    # 图片路径    
    ## $('.one-imagen img').attr('src')
    contentdiv=soup.find(attrs={"class","one-imagen"})
    picurl = contentdiv.img["src"]
    print picurl
    
    # 图片名和作者
    ## $('.one-imagen-leyenda').text()
    contentdiv=soup.find(attrs={"class","one-imagen-leyenda"})
    picnameauthor = handle_text(contentdiv.text)
    #print picnameauthor

    #每日一句
    ## $('.one-cita').text()
    contentdiv=soup.find(attrs={"class","one-cita"})
    cita=handle_text(contentdiv.text)
    #print cita

    #################文章#################
    # /article/1200
    myUrl = host+"/article/"+str(pageindex)
    result = urllib2.urlopen(urllib2.Request(myUrl))
    data = handle_response(result)
    soup = BeautifulSoup(data,'lxml')#soup = BeautifulSoup(data)
    #print soup.prettify()

    # 引言
    ## $('.comilla-cerrar').text()
    contentdiv=soup.find(attrs={"class","comilla-cerrar"})
    comilla_cerrar = handle_text(contentdiv.text)
    #print comilla_cerrar

    # 标题
    ## $('.articulo-titulo').text()
    contentdiv=soup.find(attrs={"class","articulo-titulo"})
    titulo = handle_text(contentdiv.text)
    #print titulo
    
    # 作者
    ## $('.articulo-autor').text()
    contentdiv=soup.find(attrs={"class","articulo-autor"})
    autor = handle_text(contentdiv.text)
    #print autor
    
    # 内容
    ## $('.articulo-contenido').text()
    contentdiv=soup.find(attrs={"class","articulo-contenido"})
    contenido = handle_text(contentdiv.text)
    #print contenido
    
    
    #################问题#################
    # /question/1200
    myUrl = host+"/question/"+str(pageindex)
    result = urllib2.urlopen(urllib2.Request(myUrl))
    data = handle_response(result)
    soup = BeautifulSoup(data,'lxml')#soup = BeautifulSoup(data)
    print soup.prettify()
    
    # 问题 和 回答 全部
    ## $('.one-cuestion').text()
    contentdiv=soup.find(attrs={"class","one-cuestion"})
    contentdiv.find(attrs={'class','cuestion-compartir'}).clear();
    question_qa = handle_text(contentdiv.text)
    print question_qa
    
    """
    divitr=divitr.next_sibling.next_sibling #there is a empty text between two div
    picdetail =  " ".join(divitr.get_text().split())#pic title and details
    divitr=divitr.next_sibling.next_sibling #there is a empty text between two div
    onesentence = " ".join(divitr.get_text().split())#one sentence 
    #print [pageindex,picurl,picdetail,onesentence]
    
    # #tab-articulo
    articulodiv=imagendiv.next_sibling.next_sibling
    articulodiv.find(class_="articulo-compartir").clear()#decompose() this will cause .get_text() wrong is there a bug exist?
    articulo = "\n".join(articulodiv.get_text().split())
    #print "\n".join([x.strip() for x in articulodiv.get_text().split("\n")]).strip()
    #print [articulo]
    
    # #tab-cuestion
    cuestiondiv=articulodiv.next_sibling.next_sibling
    cuestiondiv.find(class_="cuestion-compartir").clear()#decompose() this will cause .get_text() wrong is there a bug exist?
    cuestion = "\n".join(cuestiondiv.get_text().split())
    #print "\n".join([x.strip() for x in articulodiv.get_text().split("\n")]).strip()
    #print [cuestion]
    
    output = {pageindex:{
        "picurl":picurl,
        "picdetail":picdetail.encode("utf-8"),
        "onesentence":onesentence.encode("utf-8"),
        "articulo":articulo.encode("utf-8"),
        "cuestion":cuestion.encode("utf-8")
        }}
    #print output
    with open(str(pageindex)+".json", "w") as f:
        json.dump(output, f ,ensure_ascii=False,indent=0)
        #json.dump(output, f )
    hzm=picurl.split('.')[-1]
    if hzm=="jpg" or hzm=="png" or hzm=="bmp" or hzm=="jpeg" :
        saveImage(str(pageindex)+"."+hzm,picurl)
    else:
        saveImage(str(pageindex)+".jpg",picurl)
    """
    
    print_lock.acquire()
    print("get:"+str(pageindex))
    #print pageindex,leftlist
    print_lock.release()
    list_lock.acquire()
    leftlist.remove(pageindex)
    list_lock.release()
    thread.exit()

#获取 从 st 到 en 的所有内容
def getone(st,en):
    ret=getlist(range(st,en+1))
    times=1
    #检查 剩余列表 修复获取失败的
    while(len(ret)!=0):
        print("fixbug %d times" % times)
        times=times+1
        ret=getlist(ret)

#对rlist 里每个序号进行操作
def getlist(rlist):#fixbug
    global leftlist
    #初始 错误检查机制
    leftlist = []
    listold=[[] for x in range(oldlistcheck)]
    #控制 同时获取的数量
    for i in rlist:
        while True:
            list_lock.acquire()
            if len(leftlist)<threadsize :
                thread.start_new_thread(getdetail,(i,))
                leftlist.append(i)
                list_lock.release()
                break
            else:
                list_lock.release()
                time.sleep(1)
    #wait
    while True:
        list_lock.acquire()
        #完全处理完
        if len(leftlist)==0:
            print("finish!")
            list_lock.release()
            return []
        print(leftlist)
        #出错修复控制
        for j in range(oldlistcheck-1):
            listold[j]=listold[j+1]#move instead of copy
        listold[oldlistcheck-1]=leftlist[:]
        allequal=True
        for j in range(oldlistcheck-1):
            if cmp(listold[j],listold[j+1])!=0:
                allequal=False
                listold[oldlistcheck-1]
                break
        #达到设定阈值个数 全部剩余页面相同 说明这些页面卡住 返回剩余页面
        if allequal:
            list_lock.release()
            return leftlist
        list_lock.release()
        time.sleep(3)

if __name__ == '__main__':
    if isdebug:
        getone(1200,1200)
        exit();

    sten=raw_input("please input two interger(start to end):").split()
    st=int(sten[0])
    en=int(sten[1])
    getone(st,en)
    exit()
