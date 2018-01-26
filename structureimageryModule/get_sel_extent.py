from arcpy import SelectLayerByAttribute_management

def get_sel_extent(lyr, sqlquery):
    SelectLayerByAttribute_management(lyr, 'NEW_SELECTION', sqlquery)
    ext = lyr.getSelectedExtent()
    return ext

