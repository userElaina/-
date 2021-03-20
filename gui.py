import re
import time
from typing import Union
from json import loads,dumps
from os import system as sh
from random import choice as rd
from time import sleep as slp


num_type=Union[int,float,str,]
num_types=(int,float,str,)

set_type=Union[list,set,tuple,]
set_types=(list,set,tuple,)

byte_type=Union[bytes,bytearray,memoryview,]
byte_types=(bytes,bytearray,memoryview,)

bytes_type=Union[str,bytes,bytearray,memoryview,]
bytes_types=(str,bytes,bytearray,memoryview,)

in_type=Union[dict,set_type,bytes_type,]
in_types=(dict,set_type,bytes_type,)


def pt(x)->None:
	print(repr(x))

def tm()->str:
	return time.strftime('%Y%m%d%H%M%S',time.localtime())
	
def lot(l:list)->str:
	return '\n'.join([str(i) for i in l])	

def trys(c:type,s:all,default=None)->all:
	try:
		return c(s)
	except:
		return default

def test(f)->None:
	while True:
		a=input()
		if a.startswith('exit'):
			exit()
		f(a)

def jsot(
	js:dict,
	pth:str=None,
	indent:Union[int,str]='\t',
	onlyascii:bool=False,
	sort:bool=False,
	log:bool=False
)->str:
	ans=dumps(js,indent=indent,ensure_ascii=onlyascii,skipkeys=True,sort_keys=sort)
	if log:
		ans=ans.replace('\n\t','\n')[1:-1]
	if pth:
		return open(pth,'w',encoding='utf-8',errors='backslashreplace').write(ans)
	else:
		return ans

def sve(pth:str,x:all)->None:
	if isinstance(x,dict):
		return jsot(x,pth=pth,sort=True)
	if isinstance(x,set_types):
		x=lot(x)
	if isinstance(x,byte_types):
		open(pth,'wb').write(x)
	else:
		open(pth,'w',encoding='utf-8',errors='backslashreplace').write(str(x))

def opens(pth:str,s:str='')->str:
	s=''
	try:
		s=open(pth,'r',encoding='utf-8').read()
	except FileNotFoundError:
		open(pth,'w').write(s)
	return s

def openjs(pth:str)->dict:
	try:
		return loads(open(pth,'rb').read())
	except FileNotFoundError:
		open(pth,'w').write('{\n}')
	return dict()	


from PIL import ImageTk,Image
import tkinter as tk
from tkinter import scrolledtext
import queue
import threading

# import win32gui as wg
# import win32con as wc
# import win32clipboard as ww

SZX=300
SZY=300
set_rm=set()
t=None
l_pth=[None]*16
l_img=[None]*16
l_rm=list()
l_exif=list()
js=openjs('0hash8_2.json')
q=queue.Queue(maxsize=1)

n2c='qweruiopasdfjkl;'
c2n=dict()
for i in range(len(n2c)):
	c2n[n2c[i]]=i

def k_op(i:int):
	p='start '+l_pth[i]
	sh(p)
	# print(p)
	# ww.OpenClipboard()
	# ww.EmptyClipboard()
	# ww.SetClipboardData(wc.CF_UNICODETEXT,p)
	# ww.CloseClipboard()
	# wq=wg.FindWindow(None,'cmd_pic_hash')
	# wg.SendMessage(wq,wc.WM_PASTE,0,0)
	# wg.SendMessage(wq,wc.WM_KEYDOWN,wc.VK_RETURN,0)

def k_rm(i:int):
	if l_rm[i]['bg']!='red':
		set_rm.add(l_pth[i])
		print('rm '+l_pth[i])
		l_rm[i]['bg']='red'
	else:
		set_rm.discard(l_pth[i])
		print('unrm '+l_pth[i])
		l_rm[i]['bg']='white'
	
def k_listen(event):
	c=str(event.char)
	if c in c2n:
		k_rm(c2n[c])
	if c==' ':
		f_nx()

for i in range(16):
	s='def f_'+hex(i)[-1]+'():k_rm('+str(i)+')'
	exec(s)
	s='def o_'+hex(i)[-1]+'():k_op('+str(i)+')'
	exec(s)



def tk8(l:list,split_flg:str='\\',ttl:str='pic_hash'):
	global t,l_img,l_pth

	t.title(ttl)
	l_big=list()

	for i in range(16):
		try:
			l_pth[i]=l[i]
		except:
			l_pth[i]=None
			l_img[i]=None
			continue

		im=Image.open(l_pth[i])
		l_img[i]=ImageTk.PhotoImage(im.resize((SZX,SZY),Image.ANTIALIAS))

		kb=len(open(l_pth[i],'rb').read())>>10
		kx,ky=im.size
		l_big.append((kb,kx,ky))


	le=len(l_big)
	l_flg=[False]*le
	for i in range(le):
		if l_flg[i]:
			continue
		for j in range(le):
			if l_flg[j]:
				continue
			fi=1
			fj=1
			for k in range(3):
				if l_big[i][k]==l_big[j][k]:
					continue
				if l_big[i][k]<l_big[j][k]:
					fj|=2
					fi&=2
				else:
					fi|=2
					fj&=2
			if not fi:
				l_flg[i]=True
			if not fj:
				l_flg[j]=True

	for i in range(16):
		l_rm[i]['bg']='white'
		if i>=le:
			l_rm[i]['state']=tk.DISABLED
			l_rm[i]['text']=''
			continue

		l_rm[i]['state']=tk.NORMAL
		l_exif[i]['image']=l_img[i]
		l_rm[i]['text']=l_pth[i].rsplit(split_flg,1)[-1]+'\n'+str(l_big[i][1])+'x'+str(l_big[i][2])+' ('+str(l_big[i][0])+'KB) '+str(im.format)
		
		xx=i%8*310
		yy=i//8*400
		l_exif[i].place(x=xx,y=yy)
		l_rm[i].place(x=xx+10,y=yy+SZY+10)

		if l_flg[i]:
			k_rm(i)

	t.update()
	
def uq(q,split_flg:str='\\')->None:
	for i in js:
		for j in js[i]:
			if len(js[i][j])>1:
				q.put((js[i][j],split_flg,str(j)+': '+str(i)),)


def mian(f=uq,split_flg:str='\\'):
	global t,l_rm,l_exif
	_main=threading.Thread(target=f,args=(q,split_flg,))
	_main.setDaemon(True)
	_main.start()

	t=tk.Tk()
	t.geometry('2500x1080')
	
	label=tk.Label(t)
	label.focus_set()
	label.pack()

	label.bind("<Key>",k_listen)

	for i in range(16):

		l_exif.append(tk.Button(
			t,
			command=eval('o_'+hex(i)[-1]),
			height=300,
			width=300,
		))

		l_rm.append(tk.Button(
			t,
			text='Delete',
			command=eval('f_'+hex(i)[-1]),
			height=3,
			width=40,
			bg='white',
		))


	tk.Button(
		t,
		text='Next Page',
		command=f_nx,
		height=4,
		width=40,
	).place(x=2000,y=900)

	t.mainloop()

def f_nx():
	global t
	sve('0hash8_rm.txt',sorted(['file:///'+str(i) for i in set_rm]))
	if q.qsize()<=0:
		t.destroy()
	args=q.get()
	tk8(args[0],split_flg=args[1],ttl=args[2])

test_l=['test.png','test2.png',]*8

def test_uq(q,nothing_arg)->None:
	for i in range(5):
		q.put((test_l[:16-i],'\\','pic_hash'+str(i),),)

def test_mian():
	mian(test_uq)

if __name__=='__main__':
	# test_mian()
	mian(split_flg='崩')
