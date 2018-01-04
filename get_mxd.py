import arcpy, os

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'
str_strc_cent = r'PointPotentialStructureCentroids'

if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur)[0]

for lyr in df:
    print lyr.name
del(lyr)


lyr_strc_cent = arcpy.mapping.Layer(mxd_cur, str_strc_cent, df)[0]
print arcpy.GetCount_management(lyr_strc_cent)
desc = arcpy.Describe(lyr_strc_cent)

print lyr_strc_cent

fieldList = arcpy.ListFields(mxd_cur, str_strc_cent)


flds = [f.name for f in arcpy.ListFields(lyr_strc_cent)]
