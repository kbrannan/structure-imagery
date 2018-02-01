from os import path
import arcpy


def get_mxd(str_path_mxd, str_file_mxd):
    if path.isfile(str_path_mxd + "\\" + str_file_mxd):
        mxd = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    else:
        mxd = "can't find file " + str_file_mxd + " in folder " + str_path_mxd
    return mxd


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})


def make_not_vis(df):
    for lyr in df:
        if lyr.isGroupLayer:
            for lyr_g in lyr.isGroupLayer:
                lyr_g.visible = False
            del lyr_g
        else:
            lyr.visible = False


def make_vis(mxd_cur, df, listlyr):
    for str_lyr in listlyr:
        lyr_cur = arcpy.mapping.ListLayers(mxd_cur, str_lyr, df)[0]
        lyr_cur.visible = True
        arcpy.Delete_management(lyr_cur)
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()


def gen_map_images(mylist, SelLayer, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    memSelLyr = "in_memory" + "\\" + "memSelLayer"
    for curFID in mylist:
        query = '"FID" = {}'.format(curFID)
        arcpy.Select_analysis(SelLayer, memSelLyr, query)
        add_lyr = arcpy.mapping.Layer(memSelLyr)
        arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)
        arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(curFID) + '_ext_pg.png')
        arcpy.Delete_management(add_lyr)
        arcpy.Delete_management("in_memory")
        del query
