import arcpy, os

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'
str_strc_cent = r'PointPotentialStructureCentroids'

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'
str_file_image_export_prefix = 'strt_'

if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur)[0]

SelLayer = arcpy.mapping.ListLayers(mxd_cur, str_strc_cent, df)[0]

def unique_values(table , field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})

mylist = unique_values(SelLayer,'FID')

desc = arcpy.Describe(SelLayer)
fields = desc.fields
for field in fields:
    print field.aliasName

query = '"FID" = {}'.format(mylist[0])

arcpy.SelectLayerByAttribute_management(SelLayer, 'NEW_SELECTION', query)
df.zoomToSelectedFeatures()
df.panToExtent(SelLayer.getSelectedExtent())
arcpy.RefreshActiveView()
arcpy.mapping.ExportToPNG(mxd_cur, str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(myList[0]) + 'ext.png',
                                  df, df_export_width=1600, df_export_height=1600, world_file=True)

