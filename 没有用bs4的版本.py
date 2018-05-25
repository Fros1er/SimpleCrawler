# -*- coding: utf-8 -*-
from urllib import request,error
import re,codecs
class bugs:
    def __init__(self,limit=10):
        self.urls=['http://math.nutcore.net/model/']
        self.next=0
        self.all=1
        self.limit=limit
        self.islimit=True
        if limit==-1:
            self.islimit=False
    def pop(self,url):
        if url not in self.urls: #and r'.jpg' not in url:
            self.urls.append(url)
            self.all+=1
    def get(self):
        print("Next:"+self.urls[self.next])
        self.req=request.Request(self.urls[self.next])
        self.req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        try:
            with request.urlopen(self.req) as self.fu:
                self.page=self.fu.read().decode('utf-8')
        except error.HTTPError as e:
            print(e)
    def analysis(self):
        self.href=re.compile(r'href=".*"')
        self.http=re.compile(r'http.*"')
        self.clean=re.compile(r'".*"')
        for i in self.href.findall(self.page):
            self.temp=self.http.findall(i)
            if self.temp:
                self.c=self.clean.findall(self.temp[0])
                if self.c:
                    self.temp[0]=self.temp[0].replace(self.c[0],'')
                self.temp[0]=self.temp[0].replace('"','')
                self.pop(self.temp[0])
                
    def out(self):
        with codecs.open(str(self.next)+'.txt','w','utf-8') as self.f:
            self.f.write(self.urls[self.next]+'\r\n')
            self.f.write(self.page)
            self.next+=1
    def run(self):
        while self.next<self.all:
            if self.next>self.limit and islimit=True:
                break
            self.get()
            self.analysis()
            self.out()
bug=bugs()
bug.run()
print("done!")
