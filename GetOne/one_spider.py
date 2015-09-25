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
print "now you are at "+homedir

print_lock = thread.allocate_lock()
list_lock = thread.allocate_lock()
threadsize = 100
oldlistcheck = 5
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

def get_list(itemlist):
    for item in itemlist:
        print item[0].encode('utf-8')
        req = urllib2.Request(url = item[1])
        result = urllib2.urlopen(req)
        data = handle_response(result)
        soup = BeautifulSoup(data,'lxml')
        #print soup.prettify()
        infolist = soup.find_all(class_="fanhao_list_table")[0].find_all("tr")
        for eachinfo in infolist:
            #print eachinfo
            eachdetail = eachinfo.find_all(["td","th"])
            #print eachdetail
            for i in range(0,5):
                print eachdetail[i].text.encode('utf-8')+" ",
            print ""

def getdetail(pageindex):
    global leftlist
    host="http://wufazhuce.com"
    #print "获取%s..." % searchname
    #httpHandler = urllib2.HTTPHandler(debuglevel=1)
    #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    #opener = urllib2.build_opener(httpHandler, httpsHandler)
    #urllib2.install_opener(opener)
    myUrl = host+"/one/vol."+str(pageindex)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2504.0 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'29',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host': 'wufazhuce.com',
        'Referer':'http://wufazhuce.com/',
        'Upgrade-Insecure-Requests':'1'
    }
    req = urllib2.Request(myUrl)
    result = urllib2.urlopen(req)
    data = handle_response(result)
    soup = BeautifulSoup(data,'lxml')
    #print soup.prettify()
    
    # #tab-imagen
    #   <div>
    #   <div>
    #   <div>
    #   ...
    imagendiv=soup.find(id="tab-imagen")
    divitr=imagendiv.div
    picurl = divitr.img["src"]#picurl
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
    saveImage(str(pageindex)+"."+picurl.split('.')[-1],picurl)
    
    print_lock.acquire()
    print "get:"+str(pageindex)
    #print pageindex,leftlist
    print_lock.release()
    list_lock.acquire()
    leftlist.remove(pageindex)
    list_lock.release()
    thread.exit()
    
def getone(st,en):
    ret=getlist(range(st,en+1))
    times=1
    while(len(ret)!=0):
        print "fixbug %d times" % times
        times=times+1
        ret=getlist(ret)

def getlist(rlist):#fixbug
    global leftlist
    leftlist = []
    listold=[[] for x in range(oldlistcheck)]
    #print "listold",listold
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
        #thread i
        #getdetail(i)
    #wait
    while(1):
        list_lock.acquire()
        if len(leftlist)==0:
            print "finish!"
            list_lock.release()
            return []
        print leftlist
        for j in range(oldlistcheck-1):
            listold[j]=listold[j+1]#move instead of copy
        listold[oldlistcheck-1]=leftlist[:]
        allequal=True
        for j in range(oldlistcheck-1):
            if cmp(listold[j],listold[j+1])!=0:
                allequal=False
                listold[oldlistcheck-1]
                break
        if allequal:
            list_lock.release()
            return leftlist
        list_lock.release()
        time.sleep(3)

sten=raw_input("please input two interger(start to end):").split()
st=int(sten[0])
en=int(sten[1])
getone(st,en)
exit()
