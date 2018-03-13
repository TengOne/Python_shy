# coding=UTF-8
#import uniout
import sys
import io
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import time

class Test_shy:
    def __init__(self):
        #print('Init Test_shy')
        self.mp4Url=''
        self.mp4Name=''
        self.mp4Date=''
        
    def urlParse(self,url):
        #print ('urlParse',url)
        time.sleep(1)
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        #print (soup)
        for article in soup.findAll(['script']):
            if str(article).find('sources') != -1:
                #print (str(article))
                startPos = str(article).find('sources') + 21
                EndPos = str(article)[startPos:].find('\'')
                self.mp4Url = (str(article)[startPos:startPos+EndPos])
        for article in soup.findAll(['h1']):
            #print (str(article))
            startPos = str(article).find('>') + 1
            EndPos = str(article)[startPos:].find('<')
            self.mp4Name = (str(article)[startPos:startPos+EndPos])
        for article in soup.findAll(['head']):
            if str(article).find('video:release_date') != -1:
                #print (str(article))
                startPos = str(article).find('og:video:release_date') - 37
                EndPos = str(article)[startPos:].find('\"')
                mp4Date = (str(article)[startPos:startPos+EndPos])
                self.mp4Date = mp4Date[0:4]+mp4Date[5:7]+mp4Date[8:10]+mp4Date[11:13]+mp4Date[14:16]+'.'+mp4Date[17:19]
            
    def saveVideo(self,url,title,subDir):
        if url:
            try:
                fname = title + '.mp4'
                #print('fname', fname)
                path=subDir+'/'+fname
                filepath = os.path.join(subDir.encode('UTF-8'), fname.encode('UTF-8'))
                if os.path.exists(path.encode("utf-8")) is not True:
                    if url is not None:
                        urllib.request.urlretrieve(url,filepath)
                        #ir = requests.get(url, timeout=10)
                        #open(filepath, 'wb').write(ir.content)
                else:
                    site = urllib.request.urlopen(url, timeout = 3)
                    siteSize = int(site.info()['Content-Length'])
                    fileSize = os.stat(path.encode('UTF-8')).st_size
                    if fileSize < siteSize:
                        if url is not None:
                            urllib.request.urlretrieve(url,filepath)
                            #ir = requests.get(url, timeout=10)
                            #open(os.path.join(subDir.encode('UTF-8'), fname.encode('UTF-8')), 'wb').write(ir.content)
                changeTimeCmd = "touch -t "+self.mp4Date+" \""+path+"\""
                #print ("changeTimeCmd",changeTimeCmd)
                os.system(changeTimeCmd.encode("utf-8"))
            except Exception as e:
                print(e)
                #print("fail title:",title.encode("utf-8"))

    def go(self,url,subDir):
        #print ("Test_shy go")
        os.makedirs(subDir, exist_ok=True)
        self.urlParse(url)
        #print ('mp4Url:',self.mp4Url)
        #print ('mp4Name:',self.mp4Name)
        print ("mp4Date",self.mp4Date)
        self.saveVideo(self.mp4Url,self.mp4Name,subDir)

class Test_shyPage:
    def __init__(self):
        #print('Init Test_shyPage')
        self.UrlList = []

    def urlParse(self,url):
        #print ('urlParse',url)
        time.sleep(1)
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'html.parser')
        #print (soup)
        for article in soup.findAll(['li']):
            if str(article).find('class=\"title\"') != -1:
                startPos = str(article).find('class=\"title\"') + 23
                EndPos = str(article)[startPos:].find('\"')
                #print (str(article)[startPos:startPos+EndPos])
                url = "http://shyav.com"+str(article)[startPos:startPos+EndPos]
                self.UrlList.append(url)

    def goTest_shy(self,url,subDir):
        Nshy=Test_shy()
        Nshy.go(url,subDir)
        
    def go(self,url,subDir):
        os.makedirs(subDir, exist_ok=True)
        self.urlParse(url)
        #print ("Test_shyPage go")
        #for OneUrl in self.UrlList:
        for num in range(len(self.UrlList)-1,-1,-1):
            #print(self.UrlList[num])
            self.goTest_shy(self.UrlList[num],subDir)

def goFor(urlPage,sn,en,an):
    for num in range(sn,en,an):
        if num == 1:
            url = "http://shyav.com/videos/"+str(urlPage)+"/"
        else:
            url = "http://shyav.com/videos/"+str(urlPage)+"/"+str(num)+"/"
         
        print (url)
        Ndc=Test_shyPage()
        Ndc.go(str(url),str(urlPage))
            
if __name__ == "__main__":
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print ("Do SHY")
    #print ('參數個數為:', len(sys.argv), '個參數。')
    #print ('參數列表:', str(sys.argv[1]))
    
    goFor('hong-kong',2,0,-1)
    goFor('asian-webcam',2,0,-1)
    goFor('korean-bj',2,0,-1)
    goFor('china',2,0,-1)
    goFor('taiwan',2,0,-1)
    goFor('porn-movie',1,0,-1)
    
    #Ndc=Test_shyPage()
    #Ndc.go(str(sys.argv[1]),'video')
    #Nshy=Test_shy()
    #Nshy.go(str(sys.argv[1]),'asian-webcam')
 
    
