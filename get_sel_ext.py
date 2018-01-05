def get_sel_extent(mxd, lyr, df, sqlquery):
    import arcpy
    SelLayer = arcpy.mapping.ListLayers(mxd, lyr, df)[0]
    arcpy.SelectLayerByAttribute_management(SelLayer, 'NEW_SELECTION', sqlquery)
    ext = SelLayer.getSelectedExtent()
    return ext
