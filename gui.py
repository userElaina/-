s=r'C:\Users\Sakura\Pictures\1\Look\二'
dpix=2560
dpiy=1080
px=300
py=300
dx=10
dy=100

_d_b_g=False
if _d_b_g:
	s=r'C:\Users\Sakura\Desktop\try'
	dpix=1500
	dpiy=1000

from PIL import ImageTk,Image
import tkinter as tk
from tkinter import scrolledtext
import queue
import threading

# import win32gui as wg
# import win32con as wc
# import win32clipboard as ww

from tols import *
from tols import *
from tols.pictols import *


mxx=dpix//(px+dx)
mxy=(dpiy-dy)//(py+dy)
mxl=mxx*mxy
dpix=mxx*(px+dx)+dx
dpiy=mxy*(py+dy)+dy
print(mxx,mxy)

st=s.rsplit('\\',1)[-1]
j1pth='C:\\All\\Sakura\\Mili\\PY\\ahash\\d8_'+st+'_1.json'
j2pth='C:\\All\\Sakura\\Mili\\PY\\ahash\\d8_'+st+'_2.json'
rmpth='C:\\All\\Sakura\\Mili\\PY\\ahash\\d8_'+st+'_rm.txt'
lgpth='C:\\All\\Sakura\\Mili\\PY\\ahash\\d8_'+st+'_lg.log'

js=openjs(j2pth)
js_lg=0
set_rm=set()

# PTH='D:\\pixiv\\tag\\'
# x=['10000', '10000r', '20000', '20000r', '50000', '50000r']
# def get_from_wd():
# 	for i in os.walk(PTH):
# 		if i[0]==PTH:
# 			return i[1]
# 	return list()

def get_h8(pth:str=None,lv:int=6)->list():
	if not pth:
		pth=s
	nl=dict()
	for i in range(lv):
		nl[int(i)]=dict()
	
	for i in os.walk(pth):
		if 'not_hash' in i[0]:
			continue
		print(i[0])
		for j in i[2]:
			if j.rsplit('.',1)[-1].lower() not in p_end:
				continue
			pth=i[0]+'\\'+j
			n=dhash(pth)
			if n<0:
				continue
			if n not in nl[0]:
				nl[0][n]=list()
			nl[0][n].append('file:///'+pth)

	sve(j1pth,nl[0])

	print('distance 0 end')
	
	for i in list(nl[0].keys()):
		for j in list(nl[0].keys()):
			if i<=j:
				continue
			k=hm_d(i,j)
			if k>=lv:
				continue

			if i not in nl[k]:
				nl[k][i]=list()
			nl[k][i]+=nl[0][j]

			if j not in nl[k]:
				nl[k][j]=list()
			nl[k][j]+=nl[0][i]

	sve(j2pth,nl)

	print('distance',lv,'end')

l_pth=[None]*mxl
l_img=[None]*mxl
l_rm=list()
l_exif=list()

t=tk.Tk()
q=queue.Queue(maxsize=1)

n2c='qweruiopasdfjkl;'
c2n=dict()
for i in range(len(n2c)):
	c2n[n2c[i]]=i

def k_op(i:int):
	p='start '+l_pth[i]
	sh(p)
	# print(p)

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
	o='def f_'+hex(i)[-1]+'():k_rm('+str(i)+')'
	exec(o)
	o='def o_'+hex(i)[-1]+'():k_op('+str(i)+')'
	exec(o)

def f_nx()->None:
	sve(rmpth,sorted(set_rm))
	if q.qsize()<=0:
		t.destroy()
		return 
	args=q.get()
	tk8(args[0],ttl=args[1])


def tk8(l:list,ttl:str='pic_hash')->None:
	t.title(ttl)
	l_big=list()

	for i in range(mxl):
		try:
			l_pth[i]=l[i]
		except:
			l_pth[i]=None
			l_img[i]=None
			continue
		im=Image.open(l_pth[i][8:])
		l_img[i]=ImageTk.PhotoImage(im.resize((px,py),Image.ANTIALIAS))
		kb=len(open(l_pth[i][8:],'rb').read())>>10
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

	for i in range(mxl):
		l_rm[i]['bg']='white'
		if i>=le:
			l_rm[i]['state']=tk.DISABLED
			l_rm[i]['text']=''
			continue
		l_rm[i]['state']=tk.NORMAL
		l_exif[i]['image']=l_img[i]
		l_rm[i]['text']=l_pth[i].split(st,1)[-1]+'\n'+str(l_big[i][1])+'x'+str(l_big[i][2])+' ('+str(l_big[i][0])+'KB) '+str(im.format)
		xx=i%mxx*(dx+px)+dx
		yy=i//mxx*(dy+py)
		l_exif[i].place(x=xx,y=yy)
		l_rm[i].place(x=xx+dx,y=yy+py+dx)
		if l_flg[i]:
			k_rm(i)

	t.update()


def uq(q)->None:
	global js_lg
	rn=0
	for i in js:
		for j in js[i]:
			if len(js[i][j])>1:
				rn+=1
				if rn<=js_lg:
					continue
				q.put((js[i][j],str(j)+': '+str(i),))
				print(rn)
				js_lg=rn
				sve(lgpth,js_lg)


def gui(f=uq,restart=True):
	global l_rm,l_exif,js_lg,set_rm

	if not restart:
		set_rm=set([str(i) for i in opens(rmpth).split('\n') if str(i)!=''])
		js_lg=int(opens(lgpth))

	_main=threading.Thread(target=f,args=(q,))
	_main.setDaemon(True)
	_main.start()

	t.geometry(str(dpix)+'x'+str(dpiy))

	label=tk.Label(t)
	label.focus_set()
	label.pack()
	label.bind("<Key>",k_listen)

	for i in range(mxl):
		l_exif.append(tk.Button(
			t,
			command=eval('o_'+hex(i)[-1]),
			width=py,
			height=px,
		))
		l_rm.append(tk.Button(
			t,
			text='Delete',
			command=eval('f_'+hex(i)[-1]),
			width=40,
			height=3,
			bg='white',
		))

	tk.Button(
		t,
		text='Next Page',
		command=f_nx,
		width=40,
		height=4,
	).place(x=(mxx-2)*(dx+px)+(px>>1),y=mxy*(dy+py)+dx)
	t.mainloop()

def test_uq(q,nothing_arg)->None:
	test_l=['test.png','test2.png',]*mxl
	for i in range(5):
		q.put((test_l[:mxl-i],'pic_hash'+str(i),))

def test_gui():
	gui(test_uq)

def rm_one(pth:str=None):
	if not pth:
		pth=rmpth
	for i in set([str(i) for i in opens(rmpth).split('\n') if str(i)!='']):
		while i.startswith('file:///'):
			i=i[8:]
		o='del '+i
		print(o)
		sh(o)


if __name__=='__main__':
	# test_gui()

	get_h8()
	gui()
	# rm_one()

	print('end')
	
