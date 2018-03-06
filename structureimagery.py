from os import path
import arcpy

arcpy.env.workspace = arcpy.env.scratchGDB

# Locate map files, return error if not found
def get_mxd(str_path_mxd, str_file_mxd):
    if path.isfile(str_path_mxd + "\\" + str_file_mxd):
        mxd = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    else:
        mxd = "can't find file " + str_file_mxd + " in folder " + str_path_mxd
    return mxd

# Locate dataframe that includes structure layer from .mxd file
def get_df(mxd_cur, str_df_name):
    df_got = arcpy.mapping.ListDataFrames(mxd_cur, str_df_name)[0]
    return df_got

# Return a Python list of potential structures layer that exist within the .mxd file
def get_sel_layer(mxd_cur, str_poly, df_cur):
    lyr = arcpy.mapping.ListLayers(mxd_cur, str_poly, df_cur)[0]
    return lyr

# Return a sorted list of unique features
def unique_values(table, field):
   with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})

# Turn off lyr_g layer (or does this turn all layers off?)
def make_not_vis(df):
    for lyr in df:
        if lyr.isGroupLayer:
            for lyr_g in lyr.isGroupLayer:
                lyr_g.visible = False
        else:
            lyr.visible = False

# Turn on "PointPotentialStructureCentroids" layer
def make_vis(mxd_cur, df, list_lyr):
    for str_lyr in list_lyr:
        lyr_cur = arcpy.mapping.ListLayers(mxd_cur, str_lyr, df)[0]
        lyr_cur.visible = True
        #arcpy.Delete_management(lyr_cur)                                       # BTD this deletes the layer before outputting the image
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()

# Select features to extract from structure layer
def make_sel(query, str_sel_lyr):
    lyr_temp_in = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)
    lyr_temp_sel = arcpy.CreateScratchName(workspace=arcpy.env.scratchGDB)
    arcpy.MakeFeatureLayer_management(str_sel_lyr, lyr_temp_in)
    arcpy.Select_analysis(lyr_temp_sel, lyr_temp_in, query)
    return lyr_temp_sel

# Create a list of "potential structures", output a .png file of the map with potential structure polygons
def gen_map_images(my_list, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    arcpy.env.overwriteOutput = True
    for curFID in my_list:
        query = '"FID" = {}'.format(curFID)
        str_new_lyr = make_sel(query, sel_lyr.dataSource)
        add_lyr = arcpy.mapping.Layer(str_new_lyr)
        arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
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

# Create ONE map image .png file
def gen_map_image(curFID, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    arcpy.env.overwriteOutput = True                                # Set to true means tools will execute and overwrite the output dataset
    query = '"FID" = {}'.format(curFID)
    str_new_lyr = make_sel(query, sel_lyr.dataSource)               # Query the database
    add_lyr = arcpy.mapping.Layer(str_new_lyr)
    arcpy.mapping.AddLayer(df_zoom, add_lyr, "BOTTOM")
    df_zoom.panToExtent(add_lyr.getSelectedExtent())
    add_lyr.visible = True
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(curFID) + '_ext_pg.png')
    arcpy.mapping.RemoveLayer(df_zoom, add_lyr)
    arcpy.Delete_management(add_lyr)
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()

