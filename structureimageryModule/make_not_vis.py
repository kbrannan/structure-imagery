import arcpy, os

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'Upper Yaquina Near-Stream Structures (scratch).mxd'
str_df_zoom_name = r'Zoom to Feature'
str_strc_cent = r'PointPotentialStructureCentroids'
str_strc_poly = r'Potential Structures'

if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur, str_df_zoom_name)[0]

# make all layers in df not visible
for lyr in df:
    if lyr.isGroupLayer == True:
        print "Layers in " + lyr.name
    else:
        print lyr.name
        lyr.visible = False
del lyr
arcpy.RefreshTOC()
arcpy.RefreshActiveView()
mxd_cur.save()

