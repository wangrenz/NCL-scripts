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

def plot_uv(times, hgt, u, v, wsp, savepath):
	# plot
	n_time = date2num(times)
	X, Y = np.meshgrid( date2num(times), hgt)

	fig, ax = plt.subplots(figsize=(12,8),dpi=120) #figsize=(14,10)
	
	plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
	plt.rcParams['axes.unicode_minus']=False
	cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong
	ax.set_title("58141-淮安(118.92,33.63)                                                                      产品名称：风廓线",loc='left',fontsize=12,**cnfont)
	#plt.xlabel('TIME',fontsize=6)
	#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
	ax.text(-0.02, 1.012,'ALT:M',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
	#  x, y range
	ax.set_ylim(0,10230)
	ax.set_xlim(n_time[0] - (n_time[1]-n_time[0] )/4,n_time[-1] + (n_time[1]-n_time[0] )/4)
	
	ax.grid(axis='x', which='major', linewidth=0.6,linestyle='--',)
	ax.grid(axis='y', which='major', linewidth=0.6,linestyle='--',)
	
	#plt.pcolormesh(X,Y,new_vsp, cmap=plt.cm.bwr)
	# plot1 = ax.contourf(s_X,s_Y,s_vsp[:, ::-1],cmap=cmaps.MPL_BrBG,levels=np.arange(-2,2.2,0.2), extend='both' ) # GMT_polar precip3_16lev
	# clb = fig.colorbar(plot1, fraction=0.025, pad=0.01, )
	# clb.ax.tick_params(axis='y', length=0., width=0.3,direction='in',labelsize=6)
	# clb.ax.set_title('m/s',position=(1., 1))

	# cmp_flux
	#ax.barbs( X[::1, :], Y[::1, :], new_u[::1, :], new_v[::1, :], new_wsp[::1, :],cmap=plt.cm.bone_r,color='k', sizes=dict(emptybarb=0), length=6, linewidth=0.15,pivot='middle')
	ax.barbs( X[::1, :], Y[::1, :], u, v, wsp, cmap=cmaps.NCV_bright, sizes=dict(emptybarb=0), length=4.5, linewidth=0.18,pivot='middle')
	
	
	myFmt = mdates.DateFormatter('%m/%d\n%H:%M')
	#ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(25)))
	# x axis major tick , minor tick
	ax.xaxis.set_major_locator(mdates.MinuteLocator( byminute=range(0,70,10))) 
	ax.xaxis.set_minor_locator(mdates.MinuteLocator( byminute=range(0,70,5) ))
	ax.tick_params(axis="x",which='both',direction="in")
	# y axis major tick , minor tick
	ax.yaxis.set_major_locator(FixedLocator(Y[::2,0]))
	ax.yaxis.set_minor_locator(FixedLocator(Y[:,0]))
	# time axis label
	ax.xaxis.set_major_formatter(myFmt)
	
	ax.tick_params(axis='both',labelsize=6)
	fig.autofmt_xdate(rotation=0, ha='center')
	#plt.show()
	
	# save figure
	full_path = savepath + '/' + times[0].strftime("%Y%m%d")
	if not os.path.exists(full_path):
		os.makedirs(full_path)
	fig.savefig(savepath + '/' + times[0].strftime("%Y%m%d") +'/'+times[0].strftime("%Y%m%d%H%M%S") +'.png',bbox_inches='tight') #,pad_inches=0.06
#---------------------------------------------------------------------------------

def plot_uv_vvp(times, hgt, u, v, wsp, vsp, savepath):
	# plot
	n_time = date2num(times)
	X, Y = np.meshgrid( date2num(times), hgt)

	fig, ax = plt.subplots(figsize=(12,8),dpi=120) #figsize=(14,10)
	
	plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
	plt.rcParams['axes.unicode_minus']=False
	cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong
	ax.set_title("58141-淮安(118.92,33.63)                                                          产品名称：风廓线+垂直速度",loc='left',fontsize=12,**cnfont)
	#plt.xlabel('TIME',fontsize=6)
	#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
	ax.text(-0.02, 1.012,'ALT:M',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
	#  x, y range
	ax.set_ylim(0,10230)
	ax.set_xlim(n_time[0] - (n_time[1]-n_time[0] )/4,n_time[-1] + (n_time[1]-n_time[0] )/4)
	
	ax.grid(axis='x', which='major', linewidth=0.6,linestyle='--',)
	ax.grid(axis='y', which='major', linewidth=0.6,linestyle='--',)
	
	#plt.pcolormesh(X,Y,new_vsp, cmap=plt.cm.bwr)
	plot1 = ax.contourf( X, Y, vsp, cmap=cmaps.MPL_BrBG,levels=np.arange(-2,2.2,0.2), extend='both' ) # GMT_polar precip3_16lev
	clb = fig.colorbar(plot1, fraction=0.015, pad=0.01,  )
	clb.ax.tick_params(axis='y', length=0., width=0.3,direction='in',labelsize=6)
	clb.ax.set_title('m/s',position=(1., 1))

	# cmp_flux
	#ax.barbs( X[::1, :], Y[::1, :], new_u[::1, :], new_v[::1, :], new_wsp[::1, :],cmap=plt.cm.bone_r,color='k', sizes=dict(emptybarb=0), length=6, linewidth=0.15,pivot='middle')
	ax.barbs( X[::1, :], Y[::1, :], u, v, sizes=dict(emptybarb=0), length=4.5, linewidth=0.18,pivot='middle')
	
	
	myFmt = mdates.DateFormatter('%m/%d\n%H:%M')
	#ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(25)))
	# x axis major tick , minor tick
	ax.xaxis.set_major_locator(mdates.MinuteLocator( byminute=range(0,70,10))) 
	ax.xaxis.set_minor_locator(mdates.MinuteLocator( byminute=range(0,70,5) ))
	ax.tick_params(axis="x",which='both',direction="in")
	# y axis major tick , minor tick
	ax.yaxis.set_major_locator(FixedLocator(Y[::2,0]))
	ax.yaxis.set_minor_locator(FixedLocator(Y[:,0]))
	# time axis label
	ax.xaxis.set_major_formatter(myFmt)
	
	ax.tick_params(axis='both',labelsize=6)
	fig.autofmt_xdate(rotation=0, ha='center')
	#plt.show()
	
	# save figure
	full_path = savepath + '/' + times[0].strftime("%Y%m%d")
	if not os.path.exists(full_path):
		os.makedirs(full_path)
	fig.savefig(savepath + '/' + times[0].strftime("%Y%m%d") +'/'+times[0].strftime("%Y%m%d%H%M%S") +'.png',bbox_inches='tight') #,pad_inches=0.06

#---------------------------------------------------------------------------------


if __name__ == '__main__':
	
	np.set_printoptions(formatter={'float': '{: 0.2f}'.format},threshold=np.nan)

	n_t = 40     # number of read files
	datapath = "./wind/"
	savepath = "./fig_out/"
	# rad_path_list = glob.glob(datapath + "/*_O_WPRD_LC_RAD.TXT")   # rad include rds 径向速度，snr信噪比, ssw速度谱宽
	# rad_path_list.sort()     # sort file list
	# rad_list_first = rad_path_list[-n_t:]

	robs_path_list = glob.glob(datapath + "/*_P_WPRD_LC_ROBS.TXT")  # robs include  wind profile vvp
	robs_path_list.sort()
	robs_list = robs_path_list[-n_t:]
	robs_list = robs_list[::-1]
	#firstname = firstname[-1]
	times =  [ datetime.strptime( i.split('_')[4], '%Y%m%d%H%M%S')  for i in robs_list ]
	#print(times)

	new_line = [ [0 for i in range(7)] for i in range(79)]
	for it in range(n_t):
		f = open(robs_list[it],"r")
		line = f.readlines()
		for i in range(3,82):
			line[i] = line[i].replace('/','9')
			new_line[i-3][:] = line[i].split()
		del(line)
		f.close()
		data = np.array(new_line,dtype='f4')
		data[data == 99999 ] =  np.nan
		data[data == 999999 ] =  np.nan
		hgt = data[:,0]
		if it == 0:
			wdir= data[:,1]
			wsp = data[:,2]
			vsp = data[:,3]
		else:
			wdir = np.vstack((wdir,data[:,1]))
			wsp  = np.vstack((wsp,data[:,2]))
			vsp  = np.vstack((vsp,data[:,3]))
		del data
	print(wdir.shape)
	print('read data success')
	#-----------------------------------------------------------
	u   = -np.sin(np.pi * (wdir) / 180.0) * wsp
	v   = -np.cos(np.pi * (wdir) / 180.0) * wsp
	u = u * 2.5
	v = v * 2.5

	print(u)
	#plot_uv(times, hgt, u.T, v.T, wsp.T, savepath)
	plot_uv_vvp(times, hgt, u.T, v.T, wsp.T, vsp.T, savepath)
