# -*- coding: utf-8 -*-
import os
import re
import cmaps
import numpy as np
import scipy.ndimage
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator,FormatStrFormatter
from matplotlib.dates import date2num
from datetime import datetime, timedelta
import pandas as pd


def plot_fig(element, ele_val, times, savepath):
	n_time = date2num(times)
	name = elements_zh[ elements.index(element)]
	level = levels[ element ]
	#cmap = colors[ elements.index(element)]
	unit = units[elements.index(element)]
	hgt = [ [ 0.0075*i ] for i in range(ele_val.shape[1]) ]

	X, Y = np.meshgrid( date2num(times), hgt)

	fig, ax = plt.subplots(figsize=(8,8),dpi=150) #figsize=(14,10)
	
	plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
	plt.rcParams['axes.unicode_minus']=False
	cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong
	ax.set_title("58141-淮安(118.92,33.63)                           产品名称：" + name,loc='left',fontsize=12,**cnfont)
	#plt.xlabel('TIME',fontsize=6)
	#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
	ax.text(-0.035, 1.014,'ALT:km',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
	#  x, y range
	ax.set_ylim(0,Y[-1,0])
	ax.set_xlim(n_time[0] - (n_time[1]-n_time[0] )/4,n_time[-1] + (n_time[1]-n_time[0] )/4)
	
	ax.grid(axis='x', which='major', linewidth=0.6,linestyle='--',)
	ax.grid(axis='y', which='major', linewidth=0.6,linestyle='--',)
	
	#plt.pcolormesh(X,Y,new_vsp, cmap=plt.cm.bwr)
	norm = matplotlib.colors.BoundaryNorm(level,len(level))

	plot1 = ax.contourf(X, Y, np.transpose(ele_val) ,cmap=cmaps.precip3_16lev, levels=level,extend='both',norm=norm ) # GMT_polar precip3_16lev
	clb = fig.colorbar(plot1, ticks=level,fraction=0.025, pad=0.01, )
	clb.ax.tick_params(axis='y', length=0., width=0.3,direction='in',labelsize=6)
	clb.ax.set_title(unit,fontsize=8,position=(1., 1))
	
	myFmt = mdates.DateFormatter('%m/%d\n%H:%M')
	#ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(25)))
	# x axis major tick , minor tick
	ax.xaxis.set_major_locator(mdates.MinuteLocator( byminute=range(0,70,10))) 
	ax.xaxis.set_minor_locator(mdates.MinuteLocator( byminute=range(0,70,5) ))
	ax.tick_params(axis="x",which='both',direction="in")
	# y axis major tick , minor tick
	ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
	ax.yaxis.set_major_locator(FixedLocator(Y[::50,0]))
	ax.yaxis.set_minor_locator(FixedLocator(Y[::25,0]))
	# time axis label
	ax.xaxis.set_major_formatter(myFmt)
	
	ax.tick_params(axis='both',labelsize=6)
	fig.autofmt_xdate(rotation=0, ha='center')
	# save figure
	fig.savefig('last_'+ element +'.png',bbox_inches='tight') #,pad_inches=0.06

if __name__ == '__main__':
	
	n_t = 50     # number of read files
	
	global elements, elements_zh, units, colors, levels
	elements = ['extin355','extin532','depol','pm10','pm25']
	elements_zh = ['消光系数355','消光系数532','退偏振比','PM10浓度','PM2.5浓度']
	#colors = [cmaps.precip3_16lev,cmaps.precip3_16lev,cmaps.precip3_16lev,cmaps.WhBlGrYeRe,cmaps.WhBlGrYeRe]
	levels = {}
	levels['extin355'] = np.arange(0,1.1,0.1)
	levels['extin532'] = np.arange(0,1.1,0.1)
	levels['depol']    = np.arange(0,1.1,0.1)
	levels['pm10']     = np.array([0,5,10,20,30,40,50,60,70,80,90,100,200,300],dtype='f4')
	levels['pm25']     = np.array([15,20,25,30,35,40,45,50,75,115,150,200,250],dtype='f4')
	#levels['pm10']     = np.arange(0,305,5)
	#levels['pm25']     = np.arange(0,255,5)
	units = ['','','',r'$\rm mg/m^3$',r'$\rm mg/m^3$']
	ele_val = {}
	#-----longitude=0120.0;latitude=0012.0
	path="decimal"       # source data directory
	savepath="./"
	path_list=os.listdir(path)
	path_list.sort()     # sort file list
	firstname = path_list[-n_t:]
	firstname = firstname[0]
	times =  [ datetime.strptime( i.split('-')[1].split('.')[0], '%Y%m%d%H%M%S')  for i in path_list[-n_t:] ]    # datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
	
	#------------- read last number of nt files----------------- 
	for filename in path_list[-n_t:]:
		data = pd.read_csv(os.path.join(path,filename),skiprows=2,sep=';')
		for i in elements:
			if filename == firstname:
				ele_val[i] = data[i].values
			else:
				ele_val[i] = np.vstack((ele_val[i],data[i].values))
	print('read data success')
	#-----------------------------------------------------------
	for i in elements:
		plot_fig(i, ele_val[i],times, savepath)