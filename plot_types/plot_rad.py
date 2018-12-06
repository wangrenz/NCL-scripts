# -*- coding: utf-8 -*-
import os,glob
import cmaps
import numpy as np
import scipy.ndimage
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator,FormatStrFormatter
from matplotlib.dates import date2num
#import scipy.ndimage as ndimage
from datetime import datetime, timedelta

def plot_fig(ivar, mode_en, band, data, hgt,  times, savepath):  # data(hgt, time  )
	#------plot rds --------------------
	n_time = date2num(times)
	level = levels[elements[ivar]]
	color = colors[ivar]

	X, Y = np.meshgrid( date2num(times), hgt)

	fig, ax = plt.subplots(figsize=(14,8),dpi=120) #figsize=(14,10)figsize=(8,8),dpi=150
	
	plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
	plt.rcParams['axes.unicode_minus']=False
	cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong 
	ax.set_title("58141-淮安(118.92,33.63)                                  " + mode[mode_en] +"-波束"+ str(band)+ "                                       产品名称：" + elements_zh[ivar],loc='left',fontsize=12,**cnfont)
	#plt.xlabel('TIME',fontsize=6)
	#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
	ax.text(-0.02, 1.012,'ALT:M',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
	#  x, y range
	ax.set_ylim(0,10300)
	ax.set_xlim(n_time[0] - (n_time[1]-n_time[0] )/4,n_time[-1] + (n_time[1]-n_time[0] )/4)
	
	norm = matplotlib.colors.BoundaryNorm(level,len(level))

	#plot1 = ax.pcolormesh(X,Y,s_ssw, cmap=cmaps.precip3_16lev,vmin=0,vmax=17)
	plot1 = ax.contourf(X, Y, data.T ,cmap=color,levels=level, extend='both',norm=norm ) # GMT_polar precip3_16lev
	clb = fig.colorbar(plot1, fraction=0.015, pad=0.01,  )
	clb.ax.tick_params(axis='y', length=0., width=0.3,direction='in',labelsize=6)
	clb.ax.set_title(units[ivar],position=(0.6, 1))
	
	ax.grid(axis='both', which='major', linewidth=0.6,linestyle='--')
	
	myFmt = mdates.DateFormatter('%m/%d\n%H:%M')
	#ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(25)))
	# x axis major tick , minor tick
	ax.xaxis.set_major_locator(mdates.MinuteLocator( byminute=range(0,70,10))) 
	ax.xaxis.set_minor_locator(mdates.MinuteLocator( byminute=range(0,70,5) ))
	ax.tick_params(axis="x",which='both',direction="in")
	# y axis major tick , minor tick
	ax.yaxis.set_major_locator(FixedLocator(hgt[::2]))
	ax.yaxis.set_minor_locator(FixedLocator(hgt))
	# time axis label
	ax.xaxis.set_major_formatter(myFmt)
	
	ax.tick_params(axis='both',labelsize=6)
	fig.autofmt_xdate(rotation=0, ha='center')
	#plt.show()
	
	# save figure
	full_path = savepath + elements[ivar] + '/' + mode_en +'/beam' + str(band) +'/' + times[0].strftime("%Y%m%d")
	if not os.path.exists(full_path):
		os.makedirs(full_path)
	fig.savefig(savepath + elements[ivar] + '/' + mode_en +'/beam' + str(band) +'/' + times[0].strftime("%Y%m%d") +'/'+times[0].strftime("%Y%m%d%H%M%S") +'.png',bbox_inches='tight') 



#------------------------------------------------------



if __name__ == '__main__':
	
	np.set_printoptions(formatter={'float': '{: 0.2f}'.format},threshold=np.nan)

	n_t = 40     # number of read files
	datapath = "./wind/"
	savepath = "./fig_out/"

	global elements, elements_zh, units, colors,levels,mode
	elements = ['ssw','snr','rds']
	elements_zh = ['速度谱宽','信噪比','径向速度']
	units = ['m/s','dBZ','m/s']
	colors = [cmaps.precip3_16lev,cmaps.precip3_16lev,cmaps.BlueDarkRed18]
	levels = {}
	levels['ssw'] = np.arange(0,17,1)
	levels['snr'] = np.arange(0,75,5)
	levels['rds'] = np.arange(-18,20,2)
	mode = {}
	mode['low'] = "低模式"
	mode['medium'] = "中模式"
	mode['high'] = "高模式"
	#band = ['beam1','beam2','beam3']
	# rad_path_list = glob.glob(datapath + "/*_O_WPRD_LC_RAD.TXT")   # rad include rds 径向速度，snr信噪比, ssw速度谱宽
	# rad_path_list.sort()     # sort file list
	# rad_list_first = rad_path_list[-n_t:]

	rad_path_list = glob.glob(datapath + "/*_O_WPRD_LC_RAD.TXT")  # robs include  wind profile vvp
	rad_path_list.sort()
	rad_list = rad_path_list[-n_t:]
	rad_list = rad_list[::-1]
	#firstname = firstname[-1]
	times =  [ datetime.strptime( i.split('_')[4], '%Y%m%d%H%M%S')  for i in rad_list ]
	times =  [ i + timedelta(hours=8) for i in times ]
	#print(times)

	n_band = 5

	low_data = np.zeros( (n_t, n_band, 81,4),dtype='f4')
	medium_data = np.zeros( (n_t, n_band, 50, 4), dtype='f4')
	high_data = np.zeros( (n_t, n_band, 80, 4) ,dtype='f4')

	for it in range(n_t):
		f = open(rad_list[it],"r")
		line = f.readlines()
		new_line = []
		for i in range(len(line)):
			if len(line[i]) == 27:
				new_line = new_line + [ line[i].replace('/','9') ]
		del(line)
		f.close()
		line = [ i.split()   for i in new_line ]
		del(new_line)
		data = np.array(line,dtype='f4')
		data[data == 999999 ] =  np.nan
		for i in range(n_band):
			low_data[it, i, :, :] = data[i*81:(i+1)*81,:]
			medium_data[it, i, :, :] = data[i*50+405:(i+1)*50+405,:]
			high_data[it, i, :, :] = data[i*80+655:(i+1)*80+655,:]
	#---------------------------------------------------------
	print(low_data.shape)
	for ivar in range(len(elements)):
		print("plot " + elements_zh[ivar])
		for ib in range(n_band):
			print("plot band " +str(ib+1))
			plot_fig(ivar, "low", ib+1, low_data[:, ib, :, ivar+1 ],low_data[0, ib, :, 0 ], times, savepath) # ivar, data , hgt, times 
			plot_fig(ivar, "medium", ib+1, medium_data[:, ib, :, ivar+1 ],medium_data[0, ib, :, 0 ], times, savepath)
			plot_fig(ivar, "high", ib+1, high_data[:, ib, :, ivar+1 ],high_data[0, ib, :, 0 ], times, savepath)
	#plot_uv(times, hgt, u.T, v.T, wsp.T, savepath)
	#plot_fig(times, hgt, u.T, v.T, wsp.T, vsp.T, savepath)