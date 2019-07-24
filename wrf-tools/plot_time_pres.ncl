load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRF_contributed.ncl"
undef("plot_time_pres")
procedure plot_time_pres(time, wa, xlat, xlon)
local i,j
begin
    filename = flt2string(xlat) + "_" + flt2string(xlon) + "_" + cd_string(time(0), "%Y%N%D%H") + "_wa"

    xwks  = "png"
    xwks@wkWidth  = 1500
    xwks@wkHeight = 1500 
    ; xwks@wkOrientation    = "landscape"
    ;    xwks@wkPaperHeightF   = 11
    ;    xwks@wkPaperWidthF    = 6
    wks  = gsn_open_wks(xwks, filename)
    
    res                         = True
    res@gsnDraw                 = False
    res@gsnFrame                = False
    res@gsnLeftString           = cd_string(time(0), "%Y%N%D%H")
    res@gsnLeftStringFontHeightF= 0.012
    res@gsnCenterString         = "location: (" + flt2string(xlat) + ", " + flt2string(xlon) + ")"
    res@gsnCenterStringFontHeightF = 0.02
    ; res@gsnRightString          = ""
    ; res@gsnRightStringFontColor = "blue"
    res@gsnRightStringFontHeightF= 0.012
    res@gsnPaperMargin          = 0.01
    res@gsnMaximize             = True
    res@trYReverse              = True
    ; res@trXReverse              = True

    res@tiXAxisFontHeightF      = 0.016
    res@tiYAxisFontHeightF      = 0.016
    res@tmXBLabelFontHeightF    = 0.012
    res@tmYLLabelFontHeightF    = 0.012
    res@tmXBMajorLengthF        = 0.008
    res@tmYLMajorLengthF        = 0.008
    res@vpWidthF                = 1
    res@vpHeightF               = 0.5
    res@tiYAxisString           = "Pressure(hPa)"

    res@tmYLMaxTicks            = 10
    res@tmYLMinorPerMajor       = 1
    res@tmYRMinorPerMajor       = 1
    res@tmXBMinorPerMajor       = 1
    res@cnFillOn                = True
    ; res@cnFillPalette           = "WhiteGreen"
    res@cnLinesOn               = False
    res@cnLevelSelectionMode    = "ManualLevels"
    res@cnLevelSpacingF         = 0.1
    res@cnMinLevelValF          = -1
    res@cnMaxLevelValF          = 1
    res@cnSmoothingOn           = True
    res@cnSmoothingTensionF     = 0.5    ;-2.5
    res@cnSmoothingDistanceF    = 0.005  ;0.01 
    res@cnSmoothingOn           = True
    res@cnSmoothingTensionF     = 0.5    ;-2.5
    res@cnSmoothingDistanceF    = 0.005  ;0.01

    res@tmXTOn                  = False 
    res@tmYROn                  = False
    ; res@lbBoxSeparatorLinesOn   = False
    ;res@lbOrientation           = "Vertical"
    ;res@pmLabelBarWidthF        = 0.05
    res@pmLabelBarHeightF       = 0.08
    restick                     = True
    restick@ttmFormat           = "%N/%D~C~%H:%M"
    restick@ttmNumTicks         = 18
    restick@ttmMinorStride      = 0
    time_axis_labels(time, res, restick)
    printVarSummary(wa)
    plot = gsn_csm_contour(wks, wa(level|:, time|:), res)
    draw(plot)
    frame(wks)
    
    system("convert -trim +repage " + filename + ".png " + filename + ".png" )
end



begin
    wrfout_path = "../huaian/wrfout_d02_2017-08-01_00:00:00"
    wrf_f       = addfile(wrfout_path + ".nc", "r")

    wlat        = wrf_f->XLAT(0,:,:)
    wlon        = wrf_f->XLONG(0,:,:)
    times       = wrf_user_getvar(wrf_f,"times",-1)
    grid_size   = dimsizes(wlat)
    Time        = wrf_f->Times
    time       = wrf_times_c(Time,0)


    xlat = 31.737
    xlon = 118.686
    level = (/1000.,975.,950.,925.,900.,850.,800.,750.,700.,650.,600.,550.,500.,450.,400.,350.,300.,250.,200./)
    level!0 = "level"
    level&level = level
    level@units  = "hPa"

    lat = fspan(wlat(0, 0), wlat(grid_size(0)-1,grid_size(1)-1), grid_size(0))
    lon = fspan(wlon(0, 0), wlon(0,grid_size(1)-1), grid_size(1))
    lat!0 = "lat"
    lon!0 = "lon"
    lat&lat = lat
    lon&lon = lon
    lat@units = "degrees_north"
    lon@units = "degrees_east"

    p      = wrf_user_getvar(wrf_f, "pressure", -1)
    printVarSummary(p)
    wa_eta = wrf_user_getvar(wrf_f, "wa", -1)
    printVarSummary(wa_eta)
    wa_p   = wrf_user_intrp3d(wa_eta, p, "h", level, 0.,False)
    printVarSummary(wa_p)
    wa_ll  = rcm2rgrid_Wrap(wlat,wlon, wa_p, lat, lon, 0)
    wa_ll!0 = "time"
    wa_ll!1 = "level"
    wa_ll!2 = "lat"
    wa_ll!3 = "lon"
    wa_ll&time  = time
    wa_ll&level = level
    wa_ll&lat   = lat
    wa_ll&lon   = lon
    printVarSummary(wa_ll)

    plot_time_pres(time, wa_ll(:, :, {xlat}, {xlon}), xlat, xlon)


end