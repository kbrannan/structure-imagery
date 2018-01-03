import arcpy, os

str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'compare-near-streamstructures-locations-to-imagery-template20171227.mxd'


if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    df = arcpy.mapping.ListDataFrames(mxd_cur)[0]



for lyr in df:
    print lyr.name


x = 8
if x==10:
    print('X is 10')
else:
    print('Not')
