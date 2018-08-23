load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"
load "$WORKDIR/include/library.ncl"

fn = getArgsPara(params,"src")
filePart=str_split(fn,"/")
fileName=filePart(dimsizes(filePart)-1)
splitName1=str_split(fileName,".")
splitName2=splitName1(0)
;splitName=str_get_cols(splitName2,0,28)+"0000"
splitPart2=str_split(splitName2,"_")
;print(splitName)
;splitPart=str_split(splitName,"_")

model=splitPart2(1)
station=splitPart2(2)

print(model)
print(station)

splitPart1=str_split(splitName2,"-")
;print(splitPart1(1))  ; 层数
;print(splitPart1(2))  ; 时间 minutes inithours = cd_inv_calendar(inity,initm,initd,inith,0,0,units, 0)

;splitPart3 = str_split(splitPart2(dimsizes(splitPart2)-1),"-") ; end time
print(splitPart2(dimsizes(splitPart2)-2))
time1y=str_get_cols(splitPart2(dimsizes(splitPart2)-2),0,3)
time1m=str_get_cols(splitPart2(dimsizes(splitPart2)-2),4,5)  ; -2 end time
time1D=str_get_cols(splitPart2(dimsizes(splitPart2)-2),6,7)
time1H=str_get_cols(splitPart2(dimsizes(splitPart2)-2),8,9)
time1M=str_get_cols(splitPart2(dimsizes(splitPart2)-2),10,11)


time1y := toint(tostring(time1y))
time1m := toint(tostring(time1m))
time1D := toint(tostring(time1D))
time1H := toint(tostring(time1H))
time1M := toint(tostring(time1M))


;----------------------set coordinate----------------------------------------------------------------------
units = "minutes since 2018-01-01 00:00:00"
sminutes = cd_inv_calendar(time1y,time1m,time1D,time1H,time1M,0,units, 0)

time = fspan(sminutes, sminutes + toint(splitPart1(2))-1,  toint(splitPart1(2)))
time@units = units

level  = fspan(0.3,15.27,toint(splitPart1(1)))
level@units = "km"
;----------------------------------------------------------------------------------------------------------



;-------------------------------read data------------------------------------------------------------------
data  = fbindirread(fn,0,(/toint(splitPart1(1)),toint(splitPart1(2))/),"float")
data@_FillValue=-9999

data!0 = "level"
data!1 = "time"
data&level = level
data&time  = time
;------------------------------------------------------------------------------------------------------------


wks_type = "png"
;wks_type@wkOrientation    = "landscape"
;wks_type@wkPaperHeightF   = 11
;wks_type@wkPaperWidthF    = 8.5
;wks_type@wkWidth  = 900         ;工作台宽度 png figure
;wks_type@wkHeight = 900          ;工作台高度
outputPath1=getArgsPara(params,"OUTPUTDIR")
outputPath=outputPath1+"/"+splitPart2(2)+"/"+"Milliradar"+"/"+splitPart2(1)+"/"+str_get_cols(splitPart2(3),0,3)+"/"+str_get_cols(splitPart2(3),4,5)+"/"+str_get_cols(splitPart2(3),6,7)
outputfilename= splitPart2(0) + "_" + splitPart2(1) + "_" + splitPart2(2) + "_" + splitPart2(3)
checkOrCreateDir(outputPath)
wks = gsn_open_wks(wks_type,outputPath+"/"+outputfilename) 

if ( model .eq."R" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/12,1,131/),(/0,1,189/),(/3,54,233/),\
               (/0,97,253/),(/41,171,255/),(/13,220,240/),(/1,209,135/),(/0,193,63/),(/113,203,46/),\
               (/194,226,62/),(/255,255,113/),(/250,205,119/),(/247,194,82/),(/241,162,43/),(/234,110,46/),\
               (/229,40,36/),(/203,49,47/),(/127,42,39/),(/255,255,255/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."V" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/45,63,111/),(/43,106,157/),(/87,146,178/),(/64,84,56/),\
               (/55,118,97/),(/99,173,148/),(/118,198,168/),(/187,240,240/),(/229,230,250/),(/235,240,158/),(/223,211,63/),\
               (/237,153,125/),(/231,69,58/),(/255,0,0/),(/255,255,255/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."W" )then
    colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/110,122,180/),(/26,79,159/),(/37,185,171/),(/245,216,37/),(/235,90,46/),(/215,54,46/),(/255,0,0/),(/255,255,255/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq."VIL" )then
	colors = (/(/255,255,255/),(/0,0,0/),(/255,255,255/),(/4,4,100/),(/4,4,216/),(/0,255,255/),(/1,154,4/),\
               (/38,229,35/),(/255,255,5/),(/230,110,182/),(/215,18,18/),(/178,0,2/),(/133,16,193/)/)*1.0 ; we multiply by 1 to make colors float
end if

if ( model .eq. "SNR" ) then
	colors = (/ (/255,255,255/), (/1,1,103/),(/51,53,187/),(/67,68,227/),(/72,122,255/),(/75,180,218/),(/74,255,250/),(/80,255,166/), \
		(/86,252,76/),(/188,255,73/),(/227,253,74/),(/254,193,66/),(/252,103,51/),(/255,33,122/),(/249,58,169/),(/255,255,255/)  /)*1.0
end if

if ( model .eq. "LWC" ) then
	colors = (/ (/255,255,255/),(/4,4,216/),(/51,255,254/),(/2,153,6/),(/41,229,34/),(/254,255,6/),(/229,111,185/),(/211,19,18/),(/173,1,2/),(/133,18,191/),(/255,255,255/) /)*1.0
end if

cmap = colors/255.             ; normalize (required by NCL)
 setvalues NhlGetWorkspaceObjectId()
 "wsMaximumSize": 900000000
 end setvalues
gsn_define_colormap(wks, cmap)

res                             = True
res@gsnFrame                    = False            ; Don't advance the frame
res@gsnDraw                     = False            ; Don't advance the frame
res@gsnMaximize                 = True
res@gsnPaperMargin              = 0.01
res@gsnBoxMargin                = 0.01

res@cnConstFLabelOn             = False  
res@vpWidthF                    = 1
res@vpHeightF                   = 0.65
res@trYMaxF                     = 18
;res@tmXBMinorPerMajor           = 1
res@tmXBLabelFontHeightF        = 0.01

res@cnFillOn                    = True  
res@cnLinesOn                   = False
res@cnLineLabelsOn              = False
res@tmXTOn                      = False
res@tmYROn                      = False
res@gsnLeftString               = "(km)"
res@gsnLeftStringParallelPosF   = -0.06
res@gsnLeftStringOrthogonalPosF = 0.007
res@gsnLeftStringFontHeightF    = 0.02

res@lbLabelBarOn                = True
; res@lbOrientation             = "Vertical"
res@pmLabelBarHeightF           = 0.1
res@lbLabelFontHeightF          = 0.02
res@lbPerimFillColor            = 0
res@lbPerimThicknessF           = 0.1
res@lbLabelStride               = 1
res@lbBoxEndCapStyle            = "TriangleBothEnds"
res@lbTitleDirection            ="Across"
res@lbTitlePosition             = "Right"
res@lbTitleFontHeightF          = 0.012
res@lbTitleOffsetF              = 0.01
res@lbTitleExtentF              = 0.01

;res@cnRasterSmoothingOn         = True
res@cnFillMode                  = "RasterFill"
res@cnLevelSelectionMode        = "ExplicitLevels"

if model .eq."R" then
    ;res@cnLevels                =  (/32,24,18,10,2,-3,-8,-11,-14,-16,-18,-20,-23,-25,-28,-30,-33,-38,-40/)
    res@cnLevels                =  (/-40,-38,-33,-30,-28,-25,-23,-20,-18,-16,-14,-11,-8,-3,2,10,18,24,32/)
    res@cnFillColors            =  ispan(2,21,1)
    res@lbTitleString           = "(dBZ)"
end if
if model .eq."V" then
    res@cnLevels                =  (/30,8,4,2,1,0,-1,-2,-4,-6,-8,-10,-14,-20,-30/)
    res@cnFillColors            =  ispan(2,17,1)
    res@lbTitleString           = "(m/s)"
end if
if model .eq."W" then
    res@cnLevels                =  (/63,6,5,4,3,2,1,0/)
    res@cnFillColors            =  ispan(2,10,1)
    res@lbTitleString           = "(m/s)"
end if
if model .eq. "SNR" then
    res@cnLevels                =  ispan(-30,40,5)
    res@cnFillColors            =  ispan(0,15,1)
    res@lbTitleString           = "dB"
end if

if model .eq."LWC" then
    res@cnLevels                =  (/0.001, 0.01, 0.1, 0.5, 1, 4, 8, 12, 15, 18/)
    res@cnFillColors            =  ispan(0,10,1)
    res@lbTitleString           = "g/m3"
end if

;---------------set time tiack mark-------------------------
restick                     = True
restick@ttmAxis             = "XB"
restick@ttmFormat           = "%N/%D~C~%H:%M"
restick@ttmNumTicks         = 24
;restick@ttmMinorStride      = 1
time_axis_labels(time, res, restick)
;-----------------------------------------------------------

plot = gsn_csm_contour(wks, data , res)
draw(plot)
frame(wks)

print(outputPath+"/"+outputfilename)
;system("convert -rotate -90 -density 300 " + outputPath+"/"+ outputfilename + ".pdf" + "  " + outputPath+"/"+outputfilename + ".png")
system("convert  " + outputPath+"/"+ outputfilename + ".png" + "  -trim  +repage " + outputPath+"/"+outputfilename + ".png")

