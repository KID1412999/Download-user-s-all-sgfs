import requests
import codecs
from lxml import etree
s=[]
t=[]
q=[]
n=17#需要下载的页数
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
def deal_url():
	for i in range(n):
		for k in range(len(t[i])):
			q.append('http://weiqi.qq.com'+t[i][k])
	f=open('E:\\alphaleela.txt',"a")
	for l in range(len(q)):
		f.write(q[l])
		f.write("\n")
	f.close()
def download():
		for l in range(len(q)):	
			url=str(q[l])
			html=requests.get(url,headers=head)
			html.encoding="utf-8"
			ele=etree.HTML(html.text)
			st=ele.xpath("/html/body//div[@class='panel-body eidogo-player-auto modal-content']/text()")
			print(st)
			st=str(st[0])
			f=codecs.open('E:\\sgfs\\alphaleela'+str(l)+'.sgf',"w",'utf-8')
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
		t.append(st)
def product_main_url():
	for i in range(1,n+1):
		s.append('http://weiqi.qq.com/qipu/search/title/alphaleela/p/'+str(i)+'.html')
def main():
	product_main_url()
	get_url()
	deal_url()
	download()
	print('棋谱地址收集完成，总共有'+str(len(q))+'张棋谱，请打开E盘的sgfs文件夹查看！')
	exit()
if "__name__=__main__":
	main()





		
