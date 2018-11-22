#!/usr/bin/env python

import os
import json
import urllib2
from   datetime import datetime,timedelta


def filter_list(full_list):
	url_list = []
	name_list = []
	for iurl in full_list:
		for it in times:
			if it+".GRB" in iurl['FILE_NAME']:
				# loop vars
				for ikey in keys:
					if ikey in iurl['FILE_NAME']:
						# loop level
						for iv in level:
							if "100-"+iv in iurl['FILE_NAME']:
								url_list = url_list + [ iurl['FILE_URL'] ]
								name_list = name_list + [iurl['FILE_NAME'] ]
				# loop surface vars
				for ikey in srfkeys:
					if ikey in iurl['FILE_NAME']:
						url_list = url_list + [iurl['FILE_URL']]
						name_list = name_list + [iurl['FILE_NAME']]
	return url_list,name_list

def download_ec(url_list,name_list,savepath):
	os.chdir(savepath)
	print len(url_list)
	for i in range(len(url_list)):
		os.system('wget -c ' + url_list[i] + ' -O '+ name_list[i] + ' &>/dev/null &')

	return

if __name__ == "__main__":
	global keys,srfkeys,level,times
	
	keys = ['RHU' 'SHU','TEM','GPH','VVP','WIU','WIV']
	srfkeys= [ '10U','10V','DPT','PRS','SSP' ]
	level = [ '200','500', '700', '850','925','1000']
	times = [ str(x) for x in range(24,192,24)  ]
	path = "/home/ylj/ec_thin/"
	
	#-----------get time------------------
	delta = 1
	init_hour = datetime.utcnow().strftime("%H")
	if int(init_hour) > 0 and int(init_hour) <= 12:
		init_t = (datetime.utcnow() - timedelta(days=delta)).strftime("%Y%m%d") + "00"
	else:
		init_t = (datetime.utcnow() - timedelta(days=1+delta)).strftime("%Y%m%d") + "12"
	print init_t
	init_t = "2018111912"
	
	savepath = path + init_t
	if not os.path.exists(savepath):
		os.makedirs(savepath)
	#-------------------------------------
	baseUrl = 'http://10.76.89.55/cimiss-web/api?' + \
	'userId=BEJN_JNQX_ywyy' + \
	'&pwd=ywyy' + \
	'&interfaceId=getNafpFileByTimeRange' + \
	'&dataCode=NAFP_FOR_FTM_HIGH_EC_ANEA' + \
	'&timeRange=['+init_t+'0000,' + init_t +'0100]' + \
	'&dataFormat='
	
	dataFormat = 'json'
	req = urllib2.Request(baseUrl + dataFormat)
	response = urllib2.urlopen(req)
	data = response.read()
	root = json.loads(data)
    
	if root['returnCode'] == str(0):
		print root['returnMessage']
		full_list = root['DS']
		url_list,name_list = filter_list(full_list)
		download_ec(url_list,name_list,savepath)
	else:
		print "EC data not exist!"
