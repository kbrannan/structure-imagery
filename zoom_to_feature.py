import arcpy, os

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'
str_strc_cent = r'PointPotentialStructureCentroids'

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'
str_file_image_export_prefix = 'strt_'

if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur)[0]

SelLayer = arcpy.mapping.ListLayers(mxd, str_strc_cent, df)[0]

with arcpy.SearchCursor(SelLayer, ['OID@']) as cursor:
    for row in cursor:
        df.extent = row.SHAPE.extent #Set the dataframe extent to the extent of the feature
        df.scale = df.scale * 1.07 #Optionally give the shape a bit of padding around the edges
        arcpy.RefreshActiveView()
        arcpy.mapping.ExportToPNG(mxd_cur, str_path_export + str_file_image_export_prefix + '{}'.format(row[0]) + 'png',
                                  df, df_export_width=1600, df_export_height=1600, world_file=True)


