#GetOne

---

##What is this?

*Some code crawl data from wufazhuce.com*

##Usage

###GetOnePic.java

1. This code only download the pictures.
2. Modify the 109 lines of code to the path you want.
```java
///make sure the path is right and you have set up the folder
//the original code(save the picture under folder E:/one/)
savePath="E:/one/"+i+".jpg";
//For example, save picture at same folder.
savePath="./"+i+".jpg";
```
3. Execute `javac GetOnePic.java` and it will generate `GetOnePic.class`
4. Execute `java GetOnePic` Enter the start and end number of pictures and press  Enter.
5. Wait for a minute, you will get the pictures.
6. The next time you want to download the pictures again to the same path, just need start with the 4th step.

###one_spider.py

####prepare
1. [python](https://www.python.org/downloads/)**2**
2. [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

####execute
1. This code will download  all the data from each page like `http://wufazhuce.com/one/vol.1024`
2. Execute `python one_spider.py` Enter the start and end number of pictures and press Enter.
3. Wait for a minute, you will get the data in `*.json` and pictures.

##Why did I write these codes?

1. I'm interested in ONE a long time ago, but not now.
2. Exercising my code ability by writing Web Crawler.
