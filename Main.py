import requests
import codecs
import re
import os
from lxml import etree
from tkinter import *
import tkinter.messagebox
import time
s=[]
t=[]
q=[]
n=1
name="alphaleela"
def show_entry_fields():
	global name,n
	name=e1.get()
	n=int(e2.get())
	product_main_url()
	get_url()
	deal_url()
	download()
	#print('棋谱地址收集完成，总共有'+str(len(q))+'张棋谱，请打开E盘的sgfs文件夹查看！')
	tkinter.messagebox.showinfo('提示','已完成'+str(len(q))+'张棋谱的下载，请打开E盘sgfs文件夹查看！')
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
			t3=re.findall('DT\[(.+?)\]',st)
			if not os.path.exists('E://sgfs'):
				os.mkdir('E://sgfs/')
			if not os.path.exists('E://sgfs/'+name):
				os.mkdir('E://sgfs/'+name)
			f=codecs.open('E:\\sgfs\\'+name+'\\'+str(t3[0])+''+str(t1[0])+''+'VS'+''+str(t2[0])+''+str(l)+'.sgf',"w",'utf-8')
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

if "__name__=__main__":
	master = Tk()
	master.title('野狐棋谱下载器  @幻影')
	Label(master, text="请输入棋手名字：").grid(row=0)
	Label(master, text="请输入下载页数：").grid(row=1)
	e1 = Entry(master)
	e2 = Entry(master)
	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)
	Button(master, text='退出', command=master.quit).grid(row=3, column=2, sticky=W, pady=4)
	Button(master, text='开始下载', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
	Button(master, text='查询总页数', command=show_number).grid(row=3, column=0, sticky=W, pady=4)
	frame = Frame(master).grid(row =2,column =1)#使用时将框架根据情况选择新的位置
	canvas = Canvas(frame,width = 120,height = 30,bg = "white")
	canvas.grid(row =2,column =1)
	x = StringVar()
	#进度条以及完成程度
	out_rec = canvas.create_rectangle(5,5,105,25,outline = "blue",width = 1)
	fill_rec = canvas.create_rectangle(5,5,5,25,outline = "",width = 0,fill = "blue")
	Label(frame,textvariable = x).grid(row =2,column =2)
	mainloop()

