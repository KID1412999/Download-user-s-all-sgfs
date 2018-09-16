import requests
import codecs
import re
import os
from lxml import etree
from tkinter import *
import tkinter.messagebox
import time
from tkinter.filedialog import askdirectory
s=[]
t=[]
q=[]
n=1
name="alphaleela"
path_='C:'
win_b,win_w=0,0
W_=0
B_=0
def selectPath():
	global path_
	path_ = askdirectory()
	path.set(path_)
def show_entry_fields():
	global name,n
	name=e1.get()
	
	n=int(e2.get())
	product_main_url()
	get_url()
	deal_url()
	download()
	tkinter.messagebox.showinfo('提示','已完成'+str(W_+B_)+'张棋谱的下载，请前往'+path_+'//sgfs文件夹查看！')
	#exit()
def change_schedule(now_schedule,all_schedule):
	canvas.coords(fill_rec, (5, 5, 6 + (now_schedule/all_schedule)*100, 25))
	master.update()
	x.set(str(round(now_schedule/all_schedule*100,2)) + '%')
	if round(now_schedule/all_schedule*100,2) == 100.00:
		x.set("完成")
 
def show_number():
	global name
	name=e1.get()
	tkinter.messagebox.showinfo('提示',name+'共有'+check()+'页棋谱，请输入下载页数并点击下载棋谱')
head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
def deal_url():#处理棋谱地址格式
	for i in range(n):
		for k in range(len(t[i])):
			q.append('http://weiqi.qq.com'+t[i][k])
def download():#根据棋谱地址提取棋谱
	global win_b
	global win_w
	global name,W_,B_
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
		t3=re.findall('DT\[(.+?)\]',st)#提取日期
		t4=re.findall('RE\[(.+?)\]',st)#提取结果
		if t1[0]==name and t4[0][0]=='B':
			win_b+=1
		elif t2[0]==name and t4[0][0]=='W':
			win_w+=1
		if t2[0]==name:
			W_+=1
		elif t1[0]==name:
			B_+=1
		if not os.path.exists(path_+'//sgfs'):
			os.mkdir(path_+'//sgfs/')
		if not os.path.exists(path_+'//sgfs/'+name):
			os.mkdir(path_+'//sgfs/'+name)
		f=codecs.open(path_+'//sgfs//'+name+'\\'+str(t3[0])+''+str(t1[0])+''+'VS'+''+str(t2[0])+''+str(l)+'.sgf',"w",'utf-8')
		print(str(t3[0])+''+str(t1[0])+''+'VS'+''+str(t2[0])+''+str(l))
		change_schedule(l,len(q))
		f.write(st)
		f.write("\n")
		f.close()
def get_url():#构造棋谱地址
	for i in range(0,len(s)):
		url=s[i]
		html=requests.get(url,headers=head)
		html.encoding="utf-8"
		ele=etree.HTML(html.text)
		st=ele.xpath("/html//td/a/@href")
		t.append(st)
def product_main_url():#构造主地址
	for i in range(1,n+1):
		s.append('http://weiqi.qq.com/qipu/search/title/'+name+'//p/'+str(i)+'.html')
def check():#检查总页数
	url0="http://weiqi.qq.com/qipu/search/title/"+name+"//p/1.html"
	html0=requests.get(url0,headers=head)
	html0.encoding="utf-8"
	ele0=etree.HTML(html0.text)
	str0=ele0.xpath("//ul//li/a/@href")
	t0=str(str0[-1])
	t4=re.findall('p/(.+?)\.html',t0)
	return t4[0]
def show_information():
	global name,W_,B_
	t=round((win_b+win_w)*100/len(q),4)
	b=round(win_b*100/B_,2)
	w=round(win_w*100/W_,2)
	print(W_+B_,len(q))
	tkinter.messagebox.showinfo('统计'+str(W_+B_)+'局棋手信息',name+'总胜率'+str(t)+' %'+'\n执黑胜率'+str(b)+' %'+'\n执白胜率'+str(w)+' %')
	head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
	
if "__name__=__main__":
	master = Tk()
	master.title('野狐棋谱下载器  @幻影')
	Label(master, text="请输入棋手名字：").grid(row=0)
	Label(master, text="请输入下载页数：").grid(row=1)
	e1 = Entry(master,text='alphaleela')
	e2 = Entry(master,text=1)
	path = StringVar()
	e3=Entry(master, textvariable = path).grid(row =3, column =1)
	Button(master, text = "路径选择", command = selectPath).grid(row =3, column=0)
	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)
	Button(master, text='棋手信息', command=show_information).grid(row=4, column=2, sticky=W, pady=4)
	Button(master, text='开始下载', command=show_entry_fields).grid(row=4, column=1, sticky=W, pady=4)
	Button(master, text='查询总页数', command=show_number).grid(row=4, column=0, sticky=W, pady=4)
	frame = Frame(master).grid(row =2,column =1)#使用时将框架根据情况选择新的位置
	canvas = Canvas(frame,width = 120,height = 30,bg = "white")
	canvas.grid(row =2,column =1)
	x = StringVar()
	#进度条以及完成程度
	out_rec = canvas.create_rectangle(5,5,105,25,outline = "blue",width = 1)
	fill_rec = canvas.create_rectangle(5,5,5,25,outline = "",width = 0,fill = "blue")
	Label(frame,textvariable = x).grid(row =2,column =2)
	mainloop()
