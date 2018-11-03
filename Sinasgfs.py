import requests
import codecs
import re
import os
from lxml import etree
from tkinter import *
import tkinter.messagebox
import time
from urllib import parse
from tkinter.filedialog import askdirectory
s=[]
t=[]
q=[]
n=1
name="柯洁"
path_='C:'
win_b,win_w=0,0
W_=0
B_=0
c_p=[]
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
def selectPath():
	global path_
	path_ = askdirectory()
	path.set(path_)
def get_url(p):#构造棋谱地址
	global q,c_p
	q=[]
	page=p
	c_p=[]
	name_=parse.quote(name.encode('gbk'),'gbk')
	for i in range(page):
		time.sleep(1)
		url='http://duiyi.sina.com.cn/gibo/new_gibo.asp?cur_page='+str(i)+'&key=1&keyword='+name_
		html=requests.get(url,headers=head)
		html.encoding="utf-8"
		ele=etree.HTML(html.text)
		st=ele.xpath("/html//tr[@class='body_text1']/td[2]/a/@href")
		page_=ele.xpath('/html//font[@color="#CC3333"]')
		goahead=ele.xpath('/html//font[@color="#000000"]/a/@href')
		for i in st:
			q.append(i.split('\'')[1])
	print(len(q))
	#exit()
def change_schedule(now_schedule,all_schedule):
	canvas.coords(fill_rec, (5, 5, 6 + (now_schedule/all_schedule)*100, 25))
	master.update()
	x.set(str(round(now_schedule/all_schedule*100,2)) + '%')
	if round(now_schedule/all_schedule*100,2) == 100.00:
		x.set("完成")
def total_page(p):#计算page
	page=p
	name_=parse.quote(name.encode('gbk'),'gbk')
	url='http://duiyi.sina.com.cn/gibo/new_gibo.asp?cur_page='+page+'&key=1&keyword='+name_
	html=requests.get(url,headers=head)
	html.encoding="utf-8"
	ele=etree.HTML(html.text)
	st=ele.xpath("/html//tr[@class='body_text1']/td[2]/a/@href")
	page_=ele.xpath('/html//font[@color="#CC3333"]')
	goahead=ele.xpath('/html//font[@color="#000000"]/a/@href')
	try:
		goahead=re.findall('page=(.+?)&',goahead[-1])[0]#提取结果
	except:
		goahead=0
		pass
	c_p.append(len(page_))
	if int(goahead)>=len(page_) and len(page_)>9:
		total_page(goahead)
	print(sum(c_p))
def show_number():
	global name,c_p
	c_p=[]
	name=e1.get()
	if name=='':
		name='柯洁'
	total_page('0')
	tkinter.messagebox.showinfo('提示',name+'共有'+str(sum(c_p))+'页棋谱，请输入下载页数并点击下载棋谱')

def download2():
	url='http://duiyi.sina.com.cn/qipu/new_gibo.asp'
	data={'key': '2','keyword':'中国围甲22轮龙元明城杭州-浙江昆仑'}
	name=e4.get()
	data.update({'keyword':name})
	name_=parse.quote(name.encode('gbk'),'gbk')
	url='http://duiyi.sina.com.cn/gibo/new_gibo.asp?key=2&keyword='+name_
	html=requests.get(url,headers=head)
	html.encoding='gbk'
	ele=etree.HTML(html.text)
	st=ele.xpath("/html//tr[@class='body_text1']/td[2]/a/@href")
	urls=[re.findall('(http.+?sgf)',i)[0] for i in st]
	t=0
	for i in urls:
		#time.sleep(1)
		html=requests.get(i,headers=head)
		html.encoding="gbk"
		st=str(html.text)
		t1=re.findall('PB\[(.+?)\]',st)#用正则表达式提取棋手名字信息
		if len(t1)==0:
			t1=['Erro!']
		t1[0].replace('//','&')
		t2=re.findall('PW\[(.+?)\]',st)#用正则表达式提取棋手名字信息
		if len(t2)==0:
			t2=['Erro!']
		t2[0].replace('//','&')
		t3=re.findall('RD\[(.+?)\]',st)#提取日期
		if len(t3)==0:
			t3=['Erro!']
		t4=re.findall('RE\[(.+?)\]',st)#提取结果
		if len(t4)==0:
			t4=['Erro!']
		print(t1,t2,t3,t4)
		if not os.path.exists(path_+'//sgfs'):
			os.mkdir(path_+'//sgfs/')
		if not os.path.exists(path_+'//sgfs/'+name):
			os.mkdir(path_+'//sgfs/'+name)
		try:
			f=codecs.open(path_+'//sgfs//'+name+'//'+str(t3[0])+''+str(t1[0])+''+'VS'+''+str(t2[0])+''+'.sgf',"w",'utf-8')
		except:
			f=codecs.open(path_+'//sgfs//'+name+'//'+str(t3[0])+'.sgf',"w",'utf-8')
		f.write(st)
		f.close()
		change_schedule(t,len(urls))
		t+=1
	tkinter.messagebox.showinfo('提示','已完成'+str(len(q))+'张棋谱的下载，请前往'+path_+'//sgfs文件夹查看！')
def download():#根据棋谱地址提取棋谱
	global name,W_,B_,path_,win_w,win_b
	global name,n
	W_,B_,win_w,win_b=0,0,0,0
	name=e1.get()
	n=int(e2.get())
	get_url(n)
	print(q)
	t=0
	for i in q:
		#time.sleep(1)
		html=requests.get(i,headers=head)
		html.encoding="gbk"
		st=str(html.text)
		t1=re.findall('PB\[(.+?)\]',st)#用正则表达式提取棋手名字信息
		if len(t1)==0:
			t1=['Erro!']
		t1[0].replace('//','&')
		t2=re.findall('PW\[(.+?)\]',st)#用正则表达式提取棋手名字信息
		if len(t2)==0:
			t2=['Erro!']
		t2[0].replace('//','&')
		t3=re.findall('RD\[(.+?)\]',st)#提取日期
		if len(t3)==0:
			t3=['Erro!']
		t4=re.findall('RE\[(.+?)\]',st)#提取结果
		if len(t4)==0:
			t4=['Erro!']
		print(t1,t2,t3,t4)
		if t1[0]==name and t4[0][0]=='黑':
			win_b+=1
		elif t2[0]==name and t4[0][0]=='白':
			win_w+=1
		if t2[0]==name:
			W_+=1
		elif t1[0]==name:
			B_+=1
		if not os.path.exists(path_+'//sgfs'):
			os.mkdir(path_+'//sgfs/')
		if not os.path.exists(path_+'//sgfs/'+name):
			os.mkdir(path_+'//sgfs/'+name)
		try:
			f=codecs.open(path_+'//sgfs//'+name+'//'+str(t3[0])+''+str(t1[0])+''+'VS'+''+str(t2[0])+''+'.sgf',"w",'utf-8')
		except:
			f=codecs.open(path_+'//sgfs//'+name+'//'+str(t3[0])+'.sgf',"w",'utf-8')
		f.write(st)
		f.close()
		change_schedule(t,len(q))
		t+=1
	tkinter.messagebox.showinfo('提示','已完成'+str(len(q))+'张棋谱的下载，请前往'+path_+'//sgfs文件夹查看！')

def show_information():
	global name,W_,B_
	t=round((win_b+win_w)*100/len(q),4)
	b=round(win_b*100/B_,2)
	w=round(win_w*100/W_,2)
	print(W_+B_,len(q))
	tkinter.messagebox.showinfo('统计'+str(W_+B_)+'局棋手信息',name+'总胜率'+str(t)+' %'+'\n执黑胜率'+str(b)+' %'+'\n执白胜率'+str(w)+' %')
	
if "__name__=__main__":
	master = Tk()
	master.title('新浪棋谱下载器  @幻影')
	Label(master, text="请输入棋手名字：").grid(row=0)
	Label(master, text="请输入下载页数：").grid(row=1)
	Label(master, text="请输入比赛名字：").grid(row=2)
	e1 = Entry(master)
	e2 = Entry(master)
	e4 = Entry(master)
	path = StringVar()
	e3=Entry(master, textvariable = path).grid(row =3, column =1)
	Button(master, text = "路径选择", command = selectPath).grid(row =3, column=0)
	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)
	e4.grid(row=2, column=1)
	Button(master, text='棋手信息', command=show_information).grid(row=5, column=2, sticky=W, pady=4)
	Button(master, text='下载棋手', command=download).grid(row=4, column=1, sticky=W, pady=4)
	Button(master, text='下载比赛', command=download2).grid(row=4, column=2, sticky=W, pady=4)
	Button(master, text='查询总页数', command=show_number).grid(row=4, column=0, sticky=W, pady=4)
	frame = Frame(master).grid(row =2,column =1)#使用时将框架根据情况选择新的位置
	canvas = Canvas(frame,width = 120,height = 30,bg = "white")
	canvas.grid(row =6,column =1)
	x = StringVar()
	#进度条以及完成程度
	out_rec = canvas.create_rectangle(5,5,105,25,outline = "blue",width = 1)
	fill_rec = canvas.create_rectangle(5,5,5,25,outline = "",width = 0,fill = "blue")
	Label(frame,textvariable = x).grid(row =2,column =2)
	mainloop()
