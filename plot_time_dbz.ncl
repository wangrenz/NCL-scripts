load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$WORKDIR/include/library.ncl"
;坐标属性
undef ("setProperty")
procedure setProperty(olon, olat)
begin
    olon!0          = "lon"
    olon@long_name  = "lon"
    olon@units      = "degrees"
    olon&lon        = olon

    olat!0          = "lat"
    olat@long_name  = "lat"
    olat@units      = "degrees"
    olat&lat        = olat
end

;数据赋坐标
undef ("setCoordinate")
procedure setCoordinate(data,lon,lat)
begin
    data!0          = "lat"
    data&lat        = lat
        
    data!1          = "lon"
    data&lon        = lon              
end

fn = getArgsPara(params,"src")
filePart=str_split(fn,"/")
fileName=filePart(dimsizes(filePart)-1)
splitName1=str_split(fileName,".")
splitName2=splitName1(0)
splitName=str_get_cols(splitName2,0,28)+"0000"
print(splitName)
splitPart=str_split(splitName,"_")
splitPart2=str_split(splitName2,"_")

model=splitPart(1)
station=splitPart(2)
print(model)
print(station)
EndTime=str_get_cols(splitPart2(dimsizes(splitPart2)-3),0,9)

time1m=str_get_cols(splitPart2(dimsizes(splitPart2)-2),4,5)
time1D=str_get_cols(splitPart2(dimsizes(splitPart2)-2),6,7)
time1M=str_get_cols(splitPart2(dimsizes(splitPart2)-2),10,11)
time1S=str_get_cols(splitPart2(dimsizes(splitPart2)-2),12,13)
print(EndTime)
print(time1m)
print(time1D)
print(time1M)
print(time1S)
; time1=time1m+"/"+time1D+" 00:"+time1M
; time2x=getArgsPara(params,"timex")
; time2m=str_get_cols(time2x,0,1)
; time2D=str_get_cols(time2x,2,3)
; time2=time2m+"/"+time2D+" 00:"+time1M

endTime = stringtointeger(EndTime)
time_2m = str_get_cols(endTime,4,5)
time_2d = str_get_cols(endTime,6,7)
time_2h = str_get_cols(endTime,8,9)+":00"
time2   = time_2m+"/"+time_2d+" "+time_2h

intTime = 24
strTime = getpastTime(endTime,intTime)
time_1m = str_get_cols(strTime,4,5)
time_1d = str_get_cols(strTime,6,7)
time_1h = str_get_cols(strTime,8,9)+":00"
time1   = time_1m+"/"+time_1d+" "+time_1h

intTime1 = 20
strTime1 = getpastTime(endTime,intTime1)
time1h = str_get_cols(strTime1,8,9)+":00"

intTime2 = 16
strTime2 = getpastTime(endTime,intTime2)
time2h = str_get_cols(strTime2,8,9)+":00"

intTime3 = 12
strTime3 = getpastTime(endTime,intTime3)
time3h = str_get_cols(strTime3,8,9)+":00"

intTime4 = 8
strTime4 = getpastTime(endTime,intTime4)
time4h = str_get_cols(strTime4,8,9)+":00"

intTime5 = 4
strTime5 = getpastTime(endTime,intTime5)
time5h = str_get_cols(strTime5,8,9)+":00"

; time1F=toint(time1M)/60+toint(time1S)/3600
; print (time1)
; exit
splitPart1=str_split(splitName2,"-")
print(splitPart1(1))
print(splitPart1(2))
data  = fbindirread(fn,0,(/toint(splitPart1(1)),toint(splitPart1(2))/),"float")
data@_FillValue=-9999
wks_type = "png"
; wks_type@wkWidth  = 1441         ;工作台宽度
; wks_type@wkHeight = 509          ;工作台高度
outputPath1=getArgsPara(params,"OUTPUTDIR")
outputPath=outputPath1+"/"+splitPart(2)+"/"+"Milliradar"+"/"+splitPart(1)+"/"+str_get_cols(splitPart(3),0,3)+"/"+str_get_cols(splitPart(3),4,5)+"/"+str_get_cols(splitPart(3),6,7)
outputfilename=splitName(0)
checkOrCreateDir(outputPath)
wks = gsn_open_wks(wks_type,outputPath+"/"+outputfilename) 
wks_type@wkWidth  = 1200          ;工作台宽度
wks_type@wkHeight = 600         ;工作台高度  

if ( model .eq."R" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/12,1,131/),(/0,1,189/),(/3,54,233/),\
               (/0,97,253/),(/41,171,255/),(/13,220,240/),(/1,209,135/),(/0,193,63/),(/113,203,46/),\
               (/194,226,62/),(/255,255,113/),(/250,205,119/),(/247,194,82/),(/241,162,43/),(/234,110,46/),\
               (/229,40,36/),(/203,49,47/),(/127,42,39/),(/100,42,39/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."V" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/45,63,111/),(/43,106,157/),(/87,146,178/),(/64,84,56/),\
               (/55,118,97/),(/99,173,148/),(/118,198,168/),(/187,240,240/),(/229,230,250/),(/235,240,158/),(/223,211,63/),\
               (/237,153,125/),(/231,69,58/),(/255,0,0/),(/180,0,0/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."W" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/110,122,180/),(/26,79,159/),(/37,185,171/),(/245,216,37/),(/235,90,46/),(/215,54,46/),(/255,0,0/),(/180,0,0/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."VIL" )then
	colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/4,4,100/),(/4,4,216/),(/0,255,255/),(/1,154,4/),\
               (/38,229,35/),(/255,255,5/),(/230,110,182/),(/215,18,18/),(/178,0,2/),(/133,16,193/)/)*1.0 ; we multiply by 1 to make colors float
end if

cmap = colors/255.             ; normalize (required by NCL)
 setvalues NhlGetWorkspaceObjectId()
 "wsMaximumSize": 600000000
 end setvalues
; cmap="BlAqGrYeOrReVi200" 
; data!0 = "time" 
lon = fspan(0,24,toint(splitPart1(2)))
print(splitPart1(2))
; data!1 = "dis" 
lat = fspan(0,15.27,toint(splitPart1(1)))
print(splitPart1(1))
setProperty(lon,lat)
setCoordinate(data,lon,lat)
res=True
res@gsnFrame     = False            ; Don't advance the frame
res@gsnDraw      = False            ; Don't advance the frame

; 左上角坐标
res@vpXF                      = 0.08
res@vpYF                      = 0.9
res@cnInfoLabelOn               = False
res@cnConstFLabelOn             = False  
; 调节矩形的长宽
res@vpWidthF                  = 0.8
res@vpHeightF                 = 0.8
;色斑图
res@cnFillOn                    = True  
res@cnLinesOn                   = False
res@cnLineLabelsOn              = False
res@tmXTOn                    = False
res@tmYROn                    = False
res@gsnLeftString = "(km)"
res@gsnLeftStringParallelPosF =-0.06
res@gsnLeftStringOrthogonalPosF= 0.007
res@gsnLeftStringFontHeightF=0.012
;色标显示
res@lbLabelBarOn              = True
res@lbLabelAutoStride         = False
; 垂直色标条
; res@lbOrientation             = "Vertical"
; 调整色标图的大小
;res@lbPerimOn                 = False
; res@pmLabelBarWidthF          = 0.05
;res@pmLabelBarHeightF        = 0.4
res@lbLabelFontHeightF        = 0.012
res@lbPerimFillColor          = 0
res@lbPerimThicknessF         = 0.1
; cnres@lbLabelStride             = (/0,0.1,0.2,0.3,0.4,0.5/)                 ;色标标签间隔
if model.eq."R" .or. model.eq."COR" then
    res@lbLabelStrings = (/-40,-38,-33,-30,-28,-25,-23,-20,-18,-16,-14,-11,-8,-3,2,10,18,24,32/)
else if model .eq."V" then
    res@lbLabelStrings = (/-30,-20,-14,-10,-8,-6,-4,-2,-1,0,1,2,4,8,30/)
else if model .eq."W" then
    res@lbLabelStrings = (/0,1,2,3,4,5,6,63/)
; else if model .eq."VIL" then
;     res@lbLabelStrings = ispan(5,70,5)
; end if
end if
end if
end if
res@lbLabelStride  =1
; res@lbLabelOffsetF=-2.3
; res@lboff
res@lbBoxEndCapStyle ="TriangleBothEnds"
if model.eq."R" .or. model.eq."COR" then
    res@lbTitleString             = "(dBZ)"
else if model .eq."V" then
    res@lbTitleString             = "(m/s)"
else if model .eq."W" then
    res@lbTitleString             = "(m/s)"
; else if model .eq."VIL" then
;     res@lbTitleString             = "(kg/m^2)"
; end if 
end if 
end if
end if
res@lbTitleDirection          ="Across"
; res@lbTitleString             = "m/s"
res@lbTitlePosition           = "Right"
res@lbTitleFontHeightF        = 0.012
res@lbTitleOffsetF            = 0.01
res@lbTitleExtentF            = 0.01
res@tmXBMode ="Explicit"
res@tmXBLabelsOn=True
; res@tmXBValues=ispan(0, 24, 1)
; res@tmXBLabelStride=4
; res@tmXBLabels                =(/time1,"0","0","0","4:00","0","0","0","8:00","0","0","0","12:00","0","0","0","16:00","0","0","0","20:00","0","0","0",time2/)
res@tmXBValues=(/0,4+tofloat(time1M)/60,8+tofloat(time1M)/60,12+tofloat(time1M)/60,16+tofloat(time1M)/60,20+tofloat(time1M)/60,24/)
res@tmXBLabels                =(/time1,time1h,time2h,time3h,time4h,time5h,time2/)
res@tmXBLabelFontHeightF= 0.01
res@tmYLMode ="Explicit"
res@tmYLLabelsOn=True
; res@tmYLValues=(/0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15/)
; res@tmYLLabelStride=3
; res@tmYLLabels                =(/"0","0","0","3","0","0","6","0","0","9","0","0","12","0","0","15"/)
res@tmYLValues=(/3,6,9,12,15,18/)
res@tmYLLabels                =(/"3","6","9","12","15","18"/)
res@tmYLLabelFontHeightF= 0.01

; res@tmYLPrecision             = 1
; res@tmXTBorderOn              = False
; res@tmYRBorderOn              = False
; res@tmXBLabels = (/" Jan ~C~2000"," Feb ~C~2000"," Mar ~C~2000"," Apr ~C~2000", \
;                      " May ~C~2000"," Jun ~C~2000"," Jul ~C~2000"," Aug ~C~2000", \
;                      " Sep ~C~2000"," Oct ~C~2000"," Nov ~C~2000"," Dec ~C~2000", \
;                      " Jan ~C~2001"/)
; res@cnSmoothingOn               = True
; res@cnSmoothingTensionF         = 3
res@cnFillMode                ="RasterFill"
; res@cnRasterSmoothingOn = True
res@cnLevelSelectionMode = "ExplicitLevels"
if model .eq."R" then
    res@cnLevels                =  (/32,24,18,10,2,-3,-8,-11,-14,-16,-18,-20,-23,-25,-28,-30,-33,-38,-40/)
    ; res@cnLevels                =  (/-40,-38,-33,-30,-28,-25,-23,-20,-18,-16,-14,-11,-8,-3,2,10,18,24,32/)
    res@cnFillColors            =  ispan(2,21,1)
end if
if model .eq."V" then
    res@cnLevels                =  (/30,8,4,2,1,0,-1,-2,-4,-6,-8,-10,-14,-20,-30/)
    res@cnFillColors            =  ispan(2,17,1)
end if
if model .eq."W" then
    res@cnLevels                =  (/63,6,5,4,3,2,1,0/)
    res@cnFillColors            =  ispan(2,10,1)
end if
; if model .eq."VIL" then
;     res@cnLevels                =  ispan(5,70,5)
;     res@cnFillColors            =  ispan(2,16,1)
; end if


; x=min(data)
; print (x)
; exit

gsn_define_colormap(wks, cmap)
contour=gsn_csm_contour(wks, data, res)
draw(contour)
print(outputPath+"/"+outputfilename)
frame(wks)
