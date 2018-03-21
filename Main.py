import requests
import codecs
import re
from lxml import etree
s=[]
t=[]
q=[]
n=1
name="master"
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
def deal_url():
	for i in range(n):
		for k in range(len(t[i])):
			q.append('http://weiqi.qq.com'+t[i][k])
def download():
		for l in range(len(q)):	
			url=str(q[l])
			html=requests.get(url,headers=head)
			html.encoding="utf-8"
			ele=etree.HTML(html.text)
			st=ele.xpath("/html/body//div[@class='panel-body eidogo-player-auto modal-content']/text()")
			#print(st)
			st=str(st[0])
			t1=re.findall('PB\[(.+?)\]',st)#用正则表达式提取棋手名字信息
			t2=re.findall('PW\[(.+?)\]',st)#用正则表达式提取棋手名字信息
			f=codecs.open('E:\\sgfs\\'+str(t1[0])+'vs'+str(t2[0])+''+str(l)+'.sgf',"w",'utf-8')
			f.write(st)
			f.write("\n")
			f.close()
def get_url():
	for i in range(0,len(s)):
		url=s[i]
		html=requests.get(url,headers=head)
		html.encoding="utf-8"
		ele=etree.HTML(html.text)
		st=ele.xpath("/html//td/a/@href")
		print(len(st))
		t.append(st)
def product_main_url():
	for i in range(1,n+1):
		s.append('http://weiqi.qq.com/qipu/search/title/'+name+'//p/'+str(i)+'.html')
def main():
	product_main_url()
	get_url()
	deal_url()
	download()
	print('棋谱地址收集完成，总共有'+str(len(q))+'张棋谱，请打开E盘的sgfs文件夹查看！')
	exit()
if "__name__=__main__":
	name=input("请输入需要下载的棋手名字:")
	n=int(input("请输入需要下载的页数:"))
	main()





		
