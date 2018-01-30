from arcpy import mapping
from arcpy import Select_analysis, SelectLayerByAttribute_management, Delete_management

def gen_map_images(mylist, SelLayer, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    memSelLyr = "in_memory" + "\\" + "memSelLayer"
    for curFID in mylist:
        query = '"FID" = {}'.format(curFID)
        Select_analysis(SelLayer, memSelLyr, query)
        add_lyr = mapping.Layer(memSelLyr)
        mapping.AddLayer(df_zoom, add_lyr, "TOP")
        SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)
        mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')
        Delete_management(add_lyr)
        Delete_management("in_memory")
        del query
