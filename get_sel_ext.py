def get_sel_extent(mxd, lyr, df, sqlquery):
    from arcpy import SelectLayerByAttribute_management as SEL_LYR
    SEL_LYR(lyr, 'NEW_SELECTION', sqlquery)
    ext = lyr.getSelectedExtent()
    return ext


from arcpy import mapping as MAP
str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'
str_strc_cent = r'PointPotentialStructureCentroids'
str_sql = '"FID" = 5'
mxd_cur = MAP.MapDocument(str_path_mxd + "\\" + str_file_mxd)
df = MAP.ListDataFrames(mxd_cur)[0]
lyr = MAP.ListLayers(mxd_cur, str_strc_cent, df)[0]
cur_ext = get_sel_extent(mxd_cur,lyr,df,str_sql)
