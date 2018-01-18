import arcpy, os

def unique_values(table , field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})

def get_sel_extent(lyr, sqlquery):
    arcpy.SelectLayerByAttribute_management(lyr, 'CLEAR_SELECTION')
    arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION', sqlquery)
    ext = lyr.getSelectedExtent()
    return ext

def create_sel_lyr(lyr, sqlquery):
    lyr_out = 'in_memory\lyr_sel'
    arcpy.Delete_management('in_memory\lyr_sel')
    arcpy.SelectLayerByAttribute_management(lyr, 'CLEAR_SELECTION')
    arcpy.SelectLayerByAttribute_management(lyr, 'NEW_SELECTION', sqlquery)
    arcpy.CopyFeatures_management(lyr, lyr_out)

    return lyr_out

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'Upper Yaquina Near-Stream Structures (scratch).mxd'
str_df_zoom_name = r'Zoom to Feature'
str_strc_cent = r'PointPotentialStructureCentroids'

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'
str_file_image_export_prefix = 'strt_'

memSelLyr = "in_memory" + "\\" + "memSelLayer"

if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur, str_df_zoom_name)[0]
    #mxd_cur.activeView='PAGE_LAYOUT' # make sure the page layout is current view to get map with mulp data frames
    #mxd_cur.save() # have to save and then reload mxd for the change in active view to take effect
    #del mxd_cur
    #mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)

SelLayer = arcpy.mapping.ListLayers(mxd_cur, str_strc_cent, df)[0]
arcpy.Select_analysis(SelLayer, memSelLyr, "\"FID\" = 22")
add_lyr = arcpy.mapping.Layer(memSelLyr)
arcpy.mapping.AddLayer(df, add_lyr, "TOP")
df.panToExtent(add_lyr.getExtent())
SelLayer.visible = True
arcpy.RefreshActiveView()
arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')



arcpy.Delete_management("in_memory")

mylist = unique_values(SelLayer,'FID')

# make all layers no visible
for lyr in df:
    if lyr.isGroupLayer == True:
        #print "Layers in " + lyr.name
        lyr_g = arcpy.mapping.ListLayers(lyr)
        for lyr_in_g in lyr_g:
            #print lyr_in_g.name
            lyr_in_g.visible = False
        #print ""
        del lyr_in_g, lyr_g
    else:
        #print lyr.name
        lyr.visble = False
del lyr

arcpy.SelectLayerByAttribute_management(SelLayer, 'CLEAR_SELECTION')
for curFID in mylist:
    query = '"FID" = {}'.format(curFID)
    # Local variables:
PointPotentialStructureCentroids = "Near Stream Structures\\PointPotentialStructureCentroids"
PointPotentialStructureCentr = "C:\\Temp\\arcgis\\Default.gdb\\PointPotentialStructureCentr"
query = "\"FID\" = 22"

# Process: Select
arcpy.Select_analysis(SelLayer, memSelLyr, "\"FID\" = 22")
    ext_cur = get_sel_extent(SelLayer, query)
    lyr_sel0 = create_sel_lyr(SelLayer, query)
    df.panToExtent(ext_cur)
    SelLayer.visible = False
    arcpy.RefreshActiveView()
    arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')
#    arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_df.png',
#                              data_frame=df, df_export_height=1600, df_export_width=1600, world_file=True)
    del query, ext_cur, lyr_sel0


