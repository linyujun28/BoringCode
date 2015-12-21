#encoding=utf-8

# 这是什么？
# 一个简易的sjtuelearning 课件爬虫 #有诸多不完善的地方 详细见下方尚未增加的功能

# 你需要
# 0.python2 #https://www.python.org/downloads/  注意python3不是python2的更新版
# 1.beautiful soup # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
# 
# 成功运行的版本
# python: 2.7.6-8
# python-lxml: 3.3.3-1
# python-bs4: 4.2.1-1ubuntu2

# 使用说明
# 命令
# pyhton sjtuelearning.py 或 用IDLE打开按F5运行
# 输入 用户名 和 密码 登录 [见代码最下方 个人使用可直接固定字符串 以免每次运行都输入]
# 	在 课程选择 时输入q 退出
# 	在 课件选择 时 输入q 返回 课程选择

# 尚未增加功能
# 0.超时管理 # http://backup.se.sjtu.edu.cn/elearning/timeout.asp
# 1.错误登录判断
# 2.文件 下载控制 # 用户名.dat # {课名:{课件名:true/false}} # 记录数否下载
# 3.一次获取多课件页的所有内容，现在只会获取第一页的内容
# 4.在 课程选择页面支持 all
# 5.多线程并行下载

import os
import sys
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import chardet
import getpass

#father dir source url
def downsource(fdir,url):
    if url==None:
        return
    fdir="".join(fdir.split())
    if not os.path.exists(fdir):
        os.makedirs(fdir)     
    #httpHandler = urllib2.HTTPHandler(debuglevel=1)
    #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    #opener = urllib2.build_opener(httpHandler, httpsHandler)
    #urllib2.install_opener(opener)
    f = urllib2.urlopen(url[0:5]+urllib.quote(url[5:].encode('utf8'))) #skip http:
    with open(fdir+"/"+url.split('/')[-1], "wb") as code:
        code.write(f.read())

#字符串 到 整数的转换 如果错误返回-1
def safestr2int(oristr):
    try:
        ret=int(oristr)
    except ValueError:
        ret=-1
    return ret

class sjtuelearning:
    def __init__(self,uname,pwd):
        self.uname=uname
        self.pwd=pwd
    def start(self):
        while(1):
            #[[编号，课名，教师，链接]*]
            kcrt=self.kechengshuju()
            if kcrt==[]:
                print u"登录失败"
                return 
            for eachcourse in kcrt:
                print "%s %-25s %s"%(eachcourse[0],eachcourse[1],eachcourse[2])

            #输入检测 /退出
            getinput=raw_input("please input course id('q' for quit):");
            if(getinput=='q'):#退出程序
                return
            indexcourse=safestr2int(getinput)
            if(len(kcrt) <= indexcourse or indexcourse<0):
                print('index error')
                continue
            #获取 资源列表
            #[[编号,描述,链接]*] zyrt=zi yuan return
            zyrt = myModel.ziyuanliebiao(kcrt[indexcourse][3])
            if zyrt == None:
                print "教材还没有准备好，请等待一段时间。"
            else :
                while(1):
                    for eachsource in zyrt:
                        print "%s %s"%(eachsource[0],eachsource[1])
                    getinput=raw_input("please input resource id('q' for quit,'all' for download all):")
                    if(getinput=='q'):#退出课件选择 返回课程选择
                        break
                    #注意。。。。。。变量名 sssssource 和 ccccccourse
                    if(getinput=='all'):#下载所有 课件
                        for indexsource in range(len(zyrt)):
                            print "download("+str(indexsource)+"/"+str(len(zyrt))+")"
                            downsource(kcrt[indexcourse][1],zyrt[indexsource][2])
                        break
                    indexsource=safestr2int(getinput)
                    if(len(zyrt) <= indexsource or indexsource<0):
                        print('index error')
                        continue
                    #打印 课件网址
                    print zyrt[indexsource][2]
                    downsource(kcrt[indexcourse][1],zyrt[indexsource][2])
    
    def openpage(self,course_page):
        #登陆页面
        login_page = "http://backup.se.sjtu.edu.cn/elearning/logincheck.asp"
        try:
            cj = cookielib.CookieJar()
            opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2504.0 Safari/537.36')]
            data = urllib.urlencode({"loginname":self.uname,"password":self.pwd,"lang":"gb"})
            opener.open(login_page,data)
            op=opener.open(course_page)
            data= op.read()
            return data
        except Exception,e:
            print "ERROR! ",e
            return None

    def kechengshuju(self):
        #课程页面
        course_page = "http://backup.se.sjtu.edu.cn/elearning/course/courselist.asp"
        data = self.openpage(course_page)
        if data==None:
            print u"网页连接失败"
            return [];
        
        soup = BeautifulSoup(data,"lxml")
        # 如果报错lxml 用下面这句替代即可
        # soup = BeautifulSoup(data)

        xuanketr=soup.find_all(class_="tablebordercolor")[0].tr
        datatr=xuanketr.find_next_siblings("tr")
        trlen=len(datatr)
        items=[]
        for i in range(1,trlen-1):
            eachke=datatr[i]
            keming=eachke.find("td")
            jiaoshi=keming.find_next_sibling("td")
            url=keming.find('a')['href'].replace("../announcement/index.asp?courseid=","http://backup.se.sjtu.edu.cn/elearning/materials/linkredirect.asp?courseid=")+"&type=2"
            # 编号，课名，教师，链接
            items.append([i-1,keming.text,jiaoshi.text,url]) 
        return items
    
    #需要添加 翻页功能
    def ziyuanliebiao(self,ref_page):
        data = self.openpage(ref_page)
        soup = BeautifulSoup(data,"lxml")
        # 如果报错lxml 用下面这句替代即可
        # soup = BeautifulSoup(data)
        xuanketr=soup.find_all(class_="tablebordercolor")[0].tr
        datatr=xuanketr.find_next_siblings("tr")
        trlen=len(datatr)
        items=[]
        for i in range(0,trlen-1):
            eachke=datatr[i]
            txt = "".join(eachke.text.split())
            if txt=="教材还没有准备好，请等待一段时间。".decode('utf-8'):
                return None
            #参考资料说明
            cankaoziliao=eachke.find("td")
            downloadtd=cankaoziliao.find_next_sibling("td")
            if downloadtd.find('a',text="下载")==None:
                url=None
            else:
                url="http://backup.se.sjtu.edu.cn"+downloadtd.find('a',text="下载")['href']
            #[[编号,描述,链接]*]
            items.append([i," ".join(cankaoziliao.text.split()),url])
        return items

yname=raw_input("yourname:")
pwd= getpass.getpass("pwd:")
#个人使用可以 把上面两行用#注释掉 下面修改成自己的 用户名和密码即可
#yname="5130379000"
#pwd="zhelixiemima"
myModel = sjtuelearning(yname,pwd)
myModel.start()
