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


import glob
import os
import sys
from PIL import Image

EXTS = {'jpg','jpeg','gif','png','bmp'}


def phash(pth:str)->int:
	im=Image.open(pth)
	im=im.resize((8,8),Image.ANTIALIAS).convert('L')
	sm=0
	for i in im.getdata():
		sm+=int(i)
	avg=sm/64
	sm=0
	for i in im.getdata():
		sm=(sm<<1)|(1 if i<avg else 0)
	return sm

def hamming(h1:int,h2:int)->int:
    h,d=0,h1^h2
    while d:
        h+=1
        d&=d-1
    return int(h)

PTH='D:\\pixiv\\tag\\'
x=['10000', '10000r', '20000', '20000r', '50000', '50000r']
def get_from_wd():
	for i in os.walk(PTH):
		if i[0]==PTH:
			return i[1]
	return list()


def mian(pth:str,lv:int)->list():
	nl=dict()
	for i in range(lv):
		nl[int(i)]=dict()
	
	for i in os.walk(pth):
		print(i[0])
		for j in i[2]:
			if j.rsplit('.',1)[-1] not in EXTS:
				continue
			pth=i[0]+'\\'+j
			n=phash(pth)
			if n not in nl[0]:
				nl[0][n]=list()
			nl[0][n].append(pth)

	sve('0hash8_1.json',nl[0])

	print('distance 0 end')
	
	for i in list(nl[0].keys()):
		for j in list(nl[0].keys()):
			if i<=j:
				continue
			k=hamming(i,j)
			if k>=lv:
				continue

			if i not in nl[k]:
				nl[k][i]=list()
			nl[k][i]+=nl[0][j]

			if j not in nl[k]:
				nl[k][j]=list()
			nl[k][j]+=nl[0][i]

	sve('0hash8_2.json',nl)

	print('distance',lv,'end')



if __name__ == '__main__':
	s=r'C:\Users\Sakura\Pictures\1\Look\崩崩崩'
	mian(s,8)
