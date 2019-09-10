import cmaps
import numpy as np
from scipy import interpolate
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter,FixedLocator
from matplotlib.dates import date2num
#import scipy.ndimage as ndimage
from datetime import datetime, timedelta

f = open('18102920.000','r')
line = f.readlines()[4]

print(line)
dx, dy, start_lon, end_lon, start_lat, end_lat, nlon, nlat = line.split()

lon = np.arange(float(start_lon),float(end_lon)+float(dx),float(dx))
lat = np.arange(float(start_lat),float(end_lat)+float(dy),float(dy))

data = np.genfromtxt('18102920.000', skip_header=6, dtype='f4')
u = data[:int(data.shape[0]/2):,:]
v = data[:int(data.shape[0]/2):,:]
print(u.shape)
print(v.shape)
#-------58143 118.9275 33.6386---------------
points = np.array([[33.6386, 118.9275]], dtype='f4')

point_u = interpolate.interpn((lat[::-1], lon), u[::-1,:], points, method='linear')
point_v = interpolate.interpn((lat[::-1], lon), v[::-1,:], points, method='linear')
print(point_u)
print(point_v)

new_u = np.ones((11, 20))
new_v = np.ones((11, 20))
new_u = new_u * -15
new_v = new_v * -15
for i in range(new_u.shape[0]):
	for j in range(new_v.shape[1]):
		new_u[i,j] = new_u[i,j] + 3*np.sin(j) + 1/2 *np.sin(j*2)
		new_v[i,j] = new_v[i,j] + np.sin(j) + 1/2 *np.sin((j+2)*2)


new_u = new_u * 2.5
new_v = new_v * 2.5
p_level = np.array([1000,925,850,800,700,600,500,400,300,200,100],dtype='f4')
#----------100,200,300,400,500,600,700,800,850,925,1000


customdate = datetime(2018, 10, 31, 0, 00)
time = [customdate - timedelta(hours=i) for i in range(0, new_u.shape[1]*6,6)]
n_time = date2num(time)
#x_num = [ date2num(x[i]) for i in range(len(x)) ]
X, Y = np.meshgrid( date2num(time), p_level)
print(X.shape)
# plot

fig, ax = plt.subplots(figsize=(8,8),dpi=150) #figsize=(14,10)

plt.rcParams["font.sans-serif"] = 'Times New Roman' #  ["Helvetica"] #['SimHei'] Times New Roman
plt.rcParams['axes.unicode_minus']=False
cnfont = {'fontname':'SimHei'} # 楷体: KaiTi 黑体: SimHei 仿宋: FangSong
ax.set_title("58141-淮安(118.92,33.63)            产品名称：EC模式风廓线",fontsize=14,**cnfont)
#plt.xlabel('TIME',fontsize=6)
#plt.ylabel('ALT:M',fontsize=6,rotation='horizontal',position=(0.2,1.01) ) #rotation='horizontal',position=(0.2,0.01) 
ax.text(-0.035, 1.01,'level:hPa',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)
#  x, y range
# Adjust the y-axis to be logarithmic
ax.set_yscale('symlog')
ax.set_ylim(p_level.max()+30, p_level.min()-5)
#ax.set_yticklabels(Y[:,0])
#ax.set_yticks(Y[:,0])

ax.set_xlim(n_time[0] - (n_time[1]-n_time[0] )/2,n_time[-1] + (n_time[1]-n_time[0] )/2)

ax.grid(axis='x', which='major', linewidth=0.6,linestyle='--',)
ax.grid(axis='y', which='major', linewidth=0.6,linestyle='--',)

#-------------------------------------------------------------
vec1 =  ax.barbs( X[::1, :], Y[::1, :], new_u[::1, :], new_v[::1, :], np.sqrt((new_u/2.5)**2 + (new_v/2.5)**2), cmap=cmaps.NCV_jet,clim =(0, 32), sizes=dict(emptybarb=0), length=5, linewidth=0.15,pivot='middle')

bounds = range(0,36,4)
norm = matplotlib.colors.BoundaryNorm(bounds, cmaps.NCV_jet.N)

clb = plt.colorbar(vec1, cmap=cmaps.cmp_flux, norm=norm, boundaries=bounds, ticks=bounds,  extend='both', fraction=0.025, pad=0.04,)

clb.ax.tick_params(axis='y', length=0., width=0.2,direction='in',labelsize=6)
clb.ax.set_title('m/s',position=(1., 1))

myFmt = mdates.DateFormatter('%m/%d\n%H:%M')
#ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(25)))
# x axis major tick , minor tick
ax.xaxis.set_major_locator(mdates.HourLocator( byhour=range(0,24,6)))  # byhour=[0]
#ax.xaxis.set_minor_locator(mdates.HourLocator( byhour=range(0,24,6) ))
ax.tick_params(axis="x",which='both',direction="in")
# y axis major tick , minor tick
ax.yaxis.set_major_locator(FixedLocator(Y[:,0]))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
#ax.yaxis.set_minor_locator(FixedLocator(Y[:,0]))
# time axis label
ax.xaxis.set_major_formatter(myFmt)

ax.tick_params(axis='both',labelsize=6)
fig.autofmt_xdate(rotation=0, ha='center')
#plt.show()
hgt = 44306*( 1- (p_level/1013.25)**(1/5.256) ) /1000.0
ax2 = ax.twinx()
ax2.set_yscale('symlog')
ax2.set_ylim(p_level.max()+30, p_level.min()-5)
ax2.yaxis.set_major_locator(FixedLocator(Y[:,0]))
#ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
#ax2.set_yticks(Y[:,0])
hgt_n = ["%.1f" % number for number in hgt]
ax2.set_yticklabels(hgt_n)
ax2.tick_params(axis='both',labelsize=6)
ax.text(1.035, 1.01,'height:km',verticalalignment='center',horizontalalignment='center',transform=ax.transAxes,color='k', fontsize=6.5)

# save figure
fig.savefig('ec_fine_wind.png',bbox_inches='tight') #,pad_inches=0.06