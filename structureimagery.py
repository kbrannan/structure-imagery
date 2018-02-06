from os import path
import arcpy


def get_mxd(str_path_mxd, str_file_mxd):
    if path.isfile(str_path_mxd + "\\" + str_file_mxd):
        mxd = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
    else:
        mxd = "can't find file " + str_file_mxd + " in folder " + str_path_mxd
    return mxd


def get_df(mxd_cur, str_df_name):
    df_got = arcpy.mapping.ListDataFrames(mxd_cur, str_df_name)[0]
    return df_got


def get_sel_layer(mxd_cur, str_poly, df_cur):
    lyr = arcpy.mapping.ListLayers(mxd_cur, str_poly, df_cur)[0]
    #lyr_out = arcpy.mapping.Layer(lyr)
    return lyr


def unique_values(table, field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})


def make_not_vis(df):
    for lyr in df:
        if lyr.isGroupLayer:
            for lyr_g in lyr.isGroupLayer:
                lyr_g.visible = False
        else:
            lyr.visible = False


def make_vis(mxd_cur, df, list_lyr):
    for str_lyr in list_lyr:
        lyr_cur = arcpy.mapping.ListLayers(mxd_cur, str_lyr, df)[0]
        lyr_cur.visible = True
        arcpy.Delete_management(lyr_cur)
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()


def gen_map_images(my_list, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    if sel_lyr.isFeatureLayer:
        meminlyr =  "in_memory" + "\\" + "meminlayer"
        arcpy.MakeFeatureLayer_management(sel_lyr.dataSource, meminlyr)
        for curFID in my_list:
            mem_sel_lyr = "in_memory" + "\\" + "memSelLayer"
            query = '"FID" = {}'.format(curFID)
            arcpy.Select_analysis(meminlyr, mem_sel_lyr, query)
            add_lyr = arcpy.mapping.Layer(mem_sel_lyr)
            arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
            arcpy.SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)
            df_zoom.panToExtent(add_lyr.getSelectedExtent())
            # df_zoom.zoomToSelectedFeatures()
            add_lyr.visible = True
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
            arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(curFID) + '_ext_pg.png')
            arcpy.Delete_management(add_lyr)
            arcpy.Delete_management("in_memory" + "\\" + "memSelLayer")
            del query, mem_sel_lyr
    else:
        print "something ain't right"


def make_sel(curFID, sel_lyr):
    import arcpy
    query = '"FID" = {}'.format(curFID)
    mem_sel_lyr = "in_memory" + "\\" + "memSelLayer"
    meminlyr =  "in_memory" + "\\" + "memimlayer"
    arcpy.MakeFeatureLayer_management(sel_lyr.dataSource, meminlyr)
    arcpy.Select_analysis(meminlyr, mem_sel_lyr, query)
    add_lyr = arcpy.mapping.Layer(mem_sel_lyr)
    del meminlyr
    return add_lyr


def gen_map_image_single(query, cur_id, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    if sel_lyr.isFeatureLayer:
        print ""
        print "Is sel_lyr a Feature Layer = {}".format(sel_lyr.isFeatureLayer)
        print 'Query is ' + query
        print ""
        mem_sel_lyr = "in_memory" + "\\" + "memSelLayer"
        meminlyr =  "in_memory" + "\\" + "memimlayer"
        arcpy.MakeFeatureLayer_management(sel_lyr.dataSource, meminlyr)
        arcpy.Select_analysis(meminlyr, mem_sel_lyr, query)
        add_lyr = arcpy.mapping.Layer(mem_sel_lyr)
        arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
        df_zoom.zoomToSelectedFeatures()
        add_lyr.visible = True
        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix + '{}'.format(cur_id) + '_ext_pg.png')
        arcpy.Delete_management(add_lyr)
        arcpy.Delete_management("in_memory")
    else:
        print "something ain't right"

