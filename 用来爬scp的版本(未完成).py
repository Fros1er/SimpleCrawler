from bs4 import BeautifulSoup
from urllib import request,error
import re

judge=re.compile('scp\-[0-9]')
url='http://scp-wiki-cn.wikidot.com/in-the-trenches-with-the-dead'#'http://scp-wiki-cn.wikidot.com/scp-series/scp-001'
class Queue:
	def __init__(self):
		self.list=[]
		self.now=0
		self.length=0
		
	def push(self,item):
		if self.judge(item):
			self.length+=1
			self.list.append(item)
	
	def getlength(self):
		return self.length
	
	def pop(self):
		if self.now<self.length:
			self.now+=1
			return self.list[self.now-1]
		else:
			return False
	
	def judge(self,item):
		if item not in self.list and 'forum' not in item:
			return True
		else:
			return False
		
class FoundationFinder:
	def __init__(self,mainurl,url,times=10,limit=True):
		self.queue=Queue()
		self.times=times
		self.mainurl=mainurl
		self.queue.push(url)
		self.islimit=limit
		
	def gethtml(self,link):
		self.req=request.Request(link)
		#self.req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
		try:
			self.url=request.urlopen(self.req)
			self.html=self.url.read()
			self.soup=BeautifulSoup(self.html,'html.parser')
			if '此页面不存在' in self.soup.prettify():
				return 0
			else:
				return 1
		except error.HTTPError:
			return 0
		
	def getlinks(self): 
		for link in self.soup.find_all('a'):
			link=str(link.get('href'))
			if 'http' in link:
				yield link
			elif 'javascript' not in link and link!='None' and link!='/':
				yield self.mainurl+link
		
	def search(self):
		while self.queue.getlength()<self.times or self.islimit:
			link=self.queue.pop()
			if not link:
				return
			else:
				print('Now:'+link)
				if self.gethtml(link):
					with open('scp.txt','w') as f:
						for i in self.getlinks():
							self.queue.push(i)
							if judge.search(i):
								f.write(i+'\n')
				else:
				   print('404!')
				   continue
	

action=FoundationFinder('http://scp-wiki-cn.wikidot.com',url)
action.search()
