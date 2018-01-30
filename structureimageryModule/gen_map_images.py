from arcpy import mapping
from arcpy import Select_analysis, SelectLayerByAttribute_management, Delete_management

def gen_map_images(mylist, SeLayer, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix):
    memSelLyr = "in_memory" + "\\" + "memSelLayer"
    for curFID in mylist:
        query = '"FID" = {}'.format(curFID)
        arcpy.Select_analysis(SelLayer, memSelLyr, query)
        add_lyr = arcpy.mapping.Layer(memSelLyr)
        arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)
        arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')
        arcpy.Delete_management(add_lyr)
        arcpy.Delete_management("in_memory")
        del query
