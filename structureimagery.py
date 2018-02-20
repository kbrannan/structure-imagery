from os import path
from datetime import datetime
import arcpy

# Locate map files from the path given, if it is not there will return "can't find file...."
def get_mxd(str_path_mxd, str_file_mxd):
    if path.isfile(str_path_mxd + "\\" + str_file_mxd):
        mxd = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    else:
        mxd = "can't find file " + str_file_mxd + " in folder " + str_path_mxd
    return mxd

# Return data frame that includes the structure layer from current .mxd file?
def get_df(mxd_cur, str_df_name):
    df_got = arcpy.mapping.ListDataFrames(mxd_cur, str_df_name)[0]
    return df_got

# Return the structure layer from the data frame selected above from the .mxd file
def get_sel_layer(mxd_cur, str_poly, df_cur):
    lyr = arcpy.mapping.ListLayers(mxd_cur, str_poly, df_cur)[0]
    return lyr

# Search for unique value, what does "as cursor" do? Sort returned values
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})

# Find layer "isGroupLayer" and turn off this layer, making it Not visible
def make_not_vis(df):
    for lyr in df:
        if lyr.isGroupLayer:
            for lyr_g in lyr.isGroupLayer:
                lyr_g.visible = False
        else:
            lyr.visible = False

# Find structure layer and turn on this layer, making visible, update TOC and Active View
def make_vis(mxd_cur, df, list_lyr):
    for str_lyr in list_lyr:
        lyr_cur = arcpy.mapping.ListLayers(mxd_cur, str_lyr, df)[0]
        lyr_cur.visible = True
        arcpy.Delete_management(lyr_cur)
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()

# Select features to extract features from structure layer?
def make_sel(query, str_sel_lyr):
    lyr_temp_in = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)       # ? Not sure what this and following line do
    lyr_temp_sel = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)      # ?
    arcpy.MakeFeatureLayer_management(str_sel_lyr, lyr_temp_in)                 # Create a temporary feature layer "lyr_temp_in" from "str_sel_lyr"
    arcpy.Select_analysis(lyr_temp_sel, lyr_temp_in, query)                     # Extract features from new feature layer above, "lyr_temp_in" according to SQL expression
    return lyr_temp_sel

# Function will go through "my_list" and use extracted information (unsure exactly what info) to create a new structure layer that is added to the top of the dataframe.
# This layer will be made visible, then the newly added layer is deleted at the end of the function
def gen_map_images(my_list, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):         # define function "gen_map_images" where parameters are defined inside parenthesis
    arcpy.env.overwriteOutput = True
    for curFID in my_list:                                                      # What does "curFID" mean/do?
        query = '"FID" = {}'.format(curFID)                                     # What information is being extracted according to this query?
        str_new_lyr = make_sel(query, sel_lyr.dataSource)                       # Reference new layer "str_new_lyr"
        add_lyr = arcpy.mapping.Layer(str_new_lyr)                              # Create variable/reference new layer "str_new_lyr"
        arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")                         # Add new layer "str_new_lyr" to top of "df_zoom" dataframe
        df_zoom.panToExtent(add_lyr.getSelectedExtent())
        add_lyr.visible = True
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(curFID) + '_ext_pg.png')
        arcpy.mapping.RemoveLayer(df_zoom, add_lyr)
        arcpy.Delete_management(add_lyr)
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        del query, str_new_lyr, add_lyr
