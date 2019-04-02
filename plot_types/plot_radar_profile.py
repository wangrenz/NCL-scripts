# -*- coding: utf-8 -*-
import os,glob,re
import cmaps
import numpy as np
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

def plot_uv_vvp(times, hgt, u, v, wsp, vsp, saveFullname):
	# plot
	time_start = (times[-1] - timedelta(hours=3))
	n_time = date2num(times)
	X, Y = np.meshgrid( date2num(times), hgt)

	fig, ax = plt.subplots(figsize=(12,8),dpi=120) #figsize=(14,10)
	
	plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
	plt.rcParams['axes.unicode_minus']=False
	# cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong
	ax.set_title("58141",loc='left',fontsize=12, )
	#plt.xlabel('TIME',fontsize=6)
	#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
	ax.text(-0.02, 1.012,'ALT:M',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
	#  x, y range
	ax.set_ylim(0,10230)
	ax.set_xlim(time_start - (n_time[1]-n_time[0] )/4,n_time[-1] + (n_time[1]-n_time[0] )/4)
	
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
	dirname, filename = os.path.split(saveFullname)
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	fig.savefig(saveFullname, bbox_inches='tight') #,pad_inches=0.06

# --- read File ---
def readFilelist(file_list):
	n_lvl = 55
	new_line = [ [0 for i in range(7)] for i in range(n_lvl)]
	for it in range(len(file_list)):
		f = open(file_list[it],"r")
		line = f.readlines()
		for i in range(3,+n_lvl):
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
	return hgt, u, v, wsp, vsp

#---------------------------------------------------------------------------------
def getFilelist(time,str_ymd, statid):
	time_1d   = (datetime.strptime(time, '%Y%m%d%H%M%S') - timedelta(days=1) ).strftime('%Y%m%d%H%M%S')
	yy_1d = time_1d[0:4]
	mm_1d = time_1d[4:6]
	dd_1d = time_1d[6:8]
	str_ymd_1d = '/' + yy_1d + '/' + mm_1d + '/' + dd_1d + '/'
	file_list = glob.glob(datapath + statid + "/WPR_radar_n"+ str_ymd + "Z_RADA_"+ statid +"_WPRD_MOC_NWQC_ROBS_LC_QI_*.TXT")
	file_list+= glob.glob(datapath + statid + "/WPR_radar_n"+ str_ymd_1d + "Z_RADA_"+ statid +"_WPRD_MOC_NWQC_ROBS_LC_QI_*.TXT")
	file_list.sort()
	idx = file_list.index(datapath + statid + "/WPR_radar_n"+ str_ymd + "Z_RADA_"+ statid +"_WPRD_MOC_NWQC_ROBS_LC_QI_"+time+".TXT")
	file_list = file_list[0:(idx+1)]
	hgt, u, v, wsp, vsp = readFilelist(file_list)
	times =  [ datetime.strptime( re.split('[_.]',i )[-2], '%Y%m%d%H%M%S')  for i in file_list ]
	
	saveFullname = savepath + statid + "/WPR_radar_n/"+ str_ymd + "/Z_RADA_"+ statid +"_WPRD_MOC_NWQC_ROBS_LC_QI_"+ time +".png"
	plot_uv_vvp(times, hgt, u.T, v.T, wsp.T,vsp.T , saveFullname)
	return 

def postLasttime(statid):
	# "/data/WPR_radar/54399/WPR_radar_n/2019/04/01/Z_RADA_54399_WPRD_MOC_NWQC_ROBS_LC_QI_20190401010000.TXT" 
	time = datetime.utcnow().strftime('%Y%m%d%H') + '0000'
	yy = time[0:4]
	mm = time[4:6]
	dd = time[6:8]
	str_ymd = '/' + yy + '/' + mm + '/' + dd + '/'

	if os.path.exists(datapath + statid + "/WPR_radar_n/"+ str_ymd + "/Z_RADA_"+ statid +"_WPRD_MOC_NWQC_ROBS_LC_QI_"+ time +".TXT"):
		getFilelist(time, str_ymd, statid)

		
	#print(times)


	#plot_uv(times, hgt, u.T, v.T, wsp.T, savepath)




if __name__ == '__main__':
	global datapath, savepath
	stat_list = ['54399','54406','54424','54419','54421','54597','54511']
	
	# np.set_printoptions(formatter={'float': '{: 0.2f}'.format},threshold=np.nan)
	n_t = 40     # number of read files
	datapath = "/data/WPR_radar/" # 54399/WPR_radar_n/2019/04/01/"
	savepath = "/data/picture/"
	# /data/picture/54399/WPR_radar_n/
	# Z_RADA_54399_WPRD_MOC_NWQC_ROBS_LC_QI_20190401010000.TXT

	for statid in stat_list:
		postLasttime(statid)