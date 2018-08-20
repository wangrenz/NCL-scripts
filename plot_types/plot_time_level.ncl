load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"
begin
    lon = 105.75
    lat = 34.5
    units = "hours since 2018-01-01 00:00::00"
    files = systemfunc("cd ../data && ls *grib")
    filename = stringtochar(files(0))
    
    inity = stringtoshort( chartostring(filename(0:3)) )
    initm = stringtoshort( chartostring(filename(4:5)) )
    initd = stringtoshort( chartostring(filename(6:7)) )
    inith = stringtoshort( chartostring(filename(8:9)) )

    inithours = cd_inv_calendar(inity,initm,initd,inith,0,0,units, 0)


    ntime = 41
    nlevel= 19
    time       = new( ntime, "double")
    time@units = units
    level      = (/ 10, 20, 50, 70, 100, 150, 200, 250, 300, \
                   400,500,600,700, 800, 850, 900, 925, 950,1000 /)
    level@units= "hPa"

    tem = new( (/ntime, nlevel/), "float")  ;新建温度数组
    w   = new( (/ntime, nlevel/), "float")  ;垂直速度
    rh  = new( (/ntime, nlevel/), "float")  ;相对湿度
    u   = new( (/ntime, nlevel/), "float")  ;u风
    v   = new( (/ntime, nlevel/), "float")  ;v风
    tem = 1e+20
    w   = 1e+20
    rh  = 1e+20
    u   = 1e+20
    v   = 1e+20

    do ih = 0, 240, 6
        forchours = inithours + ih
        forchours@units = units
        forctimes = cd_calendar(forchours, 0)
        time(ih/6) = forchours
        print(forctimes)
        forcy = forctimes(0,0)
        forcm = forctimes(0,1)
        forcd = forctimes(0,2)
        forch = forctimes(0,3)

        path = "../data/"+ filename(0:11) + sprintf("%02.0f",forcm) + \
                sprintf("%02.0f",forcd) + sprintf("%02.0f",forch) +  ".grib"
        filestat = fileexists(path)
        if ( filestat .eq. False ) then         
           continue
        end if

        f = addfile( path, "r")
        names := getfilevarnames(f)
        varexits = 0
        do j = 0, dimsizes(names)-1
          if ( names(j) .eq. "g0_lon_4") then
            varexits = 1
          end if
        end do
        if (varexits .eq. 0) then
            continue
        end if
       
        tem(ih/6,:) = f->T_GDS0_ISBL(:,{lat},{lon})
        w(ih/6,:)   = f->W_GDS0_ISBL(:,{lat},{lon})
        rh(ih/6,:)  = f->R_GDS0_ISBL(:,{lat},{lon})
        u(ih/6,:)   = f->U_GDS0_ISBL(:,{lat},{lon})
        v(ih/6,:)   = f->V_GDS0_ISBL(:,{lat},{lon})

    end do 
    
     tem!0        = "time"
     tem!1        = "level"
     tem&time     = time
     tem&level    = level
     copy_VarCoords(tem,w)
     copy_VarCoords(tem,rh)
     copy_VarCoords(tem,u)
     copy_VarCoords(tem,v)


     xwks  = "pdf"
     xwks@wkOrientation    = "landscape"
        xwks@wkPaperHeightF   = 11
        xwks@wkPaperWidthF    = 6
     wks  = gsn_open_wks(xwks,"init" + inity+ filename(0:5) + "rh")

     res                         = True
     res@gsnDraw                 = False
     res@gsnFrame                = False
     res@gsnLeftString           = "Vertical velocity:  < -2 x 10 Pa/s"
     res@gsnLeftStringFontHeightF= 0.01
     res@gsnCenterString          = ""
     res@gsnRightString          = "lon=" + lon +"  lat=" + lat
     res@gsnRightStringFontColor = "blue"
     res@gsnRightStringFontHeightF= 0.02
     res@gsnPaperMargin          = 0.01
     res@gsnMaximize             = True
     res@trYReverse              = True
     res@trXReverse              = True
     res@tiXAxisFontHeightF      = 0.008
     res@tmXBLabelFontHeightF    = 0.008
     res@vpWidthF                = 1
     res@vpHeightF               = 0.45
     res@tiYAxisString           = ""

     res@tmYLMaxTicks            = 10
     res@tmYLMinorPerMajor       = 1
     res@tmYRMinorPerMajor       = 1
     res@tmXBMinorPerMajor       = 1


     res@cnFillOn                = True
     res@cnFillPalette           = "WhiteGreen"
     res@cnLinesOn               = False
     res@cnLevelSelectionMode    = "ExplicitLevels"
     res@cnLevels                = (/ 70, 80, 90, 95, 98 /)  
     res@cnSmoothingOn           = True
     res@cnSmoothingTensionF     = 0.5    ;-2.5
     res@cnSmoothingDistanceF    = 0.005  ;0.01
 
     res@lbBoxSeparatorLinesOn   = False
     ;res@lbOrientation           = "Vertical"
     ;res@pmLabelBarWidthF        = 0.05
     res@pmLabelBarHeightF       = 0.05

     restick                     = True
     restick@ttmFormat           = "%N/%D ~C~ %H:%M"
     restick@ttmNumTicks         = 18
     restick@ttmMinorStride      = 0
     time_axis_labels(time, res, restick)

     print(time)
     printVarSummary(rh)
     rh := rh(:,{100:900:})
     plot = gsn_csm_contour(wks, rh(level|:,time|:), res)

    wres                        = True
    wres@gsnDraw                = False
    wres@gsnFrame               = False
    wres@gsnLeftString              = ""
    wres@gsnRightString             = ""
    wres@vcGlyphStyle               = "WindBarb"
    wres@vcWindBarbLineThicknessF   = 0.6
    wres@vcWindBarbColor            = "black"
    wres@vcRefLengthF               = 0.02 ;0.045
    wres@vcRefMagnitudeF            = 10
    wres@vcRefAnnoOn                = True
    wres@vcRefAnnoString1           = "4 m/s"
    wres@vcRefAnnoSide              = "Top"
    wres@vcRefAnnoString2On         = False
    wres@vcRefAnnoPerimOn           = False
    wres@vcRefAnnoOrthogonalPosF    = -1.37
    wres@vcRefAnnoParallelPosF      = 1;0.999
    wres@vcRefAnnoBackgroundColor   = "gray90"
    wres@vcMinDistanceF             = 0.012
    wres@vcMapDirection             = False
    u := u(:,{100:900:})
    u  = u * 2.5
    v := v(:,{100:900:})
    v  = v * 2.5
    
    plot_wind = gsn_csm_vector(wks,u(level|:,time|:),v(level|:,time|:), wres)
    
    tres                         = True
    tres@gsnDraw                 = False
    tres@gsnFrame                = False
    tres@gsnLeftString           = ""
    tres@gsnRightString          = ""
    tres@cnFillOn                = False
    tres@cnLineLabelInterval     = 1
    tres@cnLineColor             = "red";"midnightblue" ;mediumblue
    tres@cnLineLabelFontHeightF  = 0.005
    tres@cnLineLabelFontColor    = "red"
    tres@cnLineThicknessF        = 1
    tres@cnLineLabelBackgroundColor= 0
    ;tres@cnLineDashPattern       = 6
    tres@cnLevelSpacingF         = 4
    tres@cnSmoothingOn           = True
    tres@cnSmoothingTensionF     = 0.5    ;-2.5
    tres@cnSmoothingDistanceF    = 0.005  ;0.01
    tres@cnInfoLabelOn           = False
    tem := tem(:,{100:900:})
    tem = tem - 273.15
    plot_tem = gsn_csm_contour(wks,tem(level|:,time|:) , tres)

    sres                         = True
    sres@gsnDraw                 = False
    sres@gsnFrame                = False
    sres@gsnLeftString           = ""
    sres@gsnRightString          = ""
    sres@cnFillOn                = False
    sres@cnLineLabelInterval     = 1
    sres@cnLineColor             = "midnightblue" ;mediumblue
    sres@cnLineLabelFontHeightF  = 0.005
    sres@cnLineLabelFontColor    = "blue"
    sres@cnLineThicknessF        = 2
    sres@cnLineLabelBackgroundColor= 0
    ;sres@cnLineDashPattern       = 5
    sres@cnLevelSelectionMode    = "ManualLevels"
    sres@cnLevelSpacingF         = 2
    sres@cnMinLevelValF          = -20
    sres@cnMaxLevelValF          = -2
    sres@cnSmoothingOn           = True
    sres@cnSmoothingTensionF     = 0.5    ;-2.5
    sres@cnSmoothingDistanceF    = 0.005  ;0.01
    sres@cnInfoLabelOn           = False
    w := w(:,{100:900:})
    w  = w * 10.0
    plot_w = gsn_csm_contour(wks,w(level|:,time|:) , sres)

    overlay(plot,plot_tem )    
    overlay(plot,plot_wind)
    overlay(plot,plot_w   )
    draw(wks)

end
