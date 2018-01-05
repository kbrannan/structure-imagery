def get_sel_extent(mxd, lyr, df, sqlquery):
    str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
    str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'
    str_strc_cent = r'PointPotentialStructureCentroids'

    from arcpy import mapping as MAP
    from arcpy import SelectLayerByAttribute_management as SEL_LYR
    mxd_cur = MAP.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = MAP.ListDataFrames(mxd_cur)[0]
    SelLayer = MAP.ListLayers(mxd, lyr, df)[0]
    sqlquery = '"FID" = {}'.format(mylist[0])
    SEL_LYR(SelLayer, 'NEW_SELECTION', sqlquery)
    ext = SelLayer.getSelectedExtent()
    return ext
