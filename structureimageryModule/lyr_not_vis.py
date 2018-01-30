from arcpy import mapping
from arcpy import RefreshTOC

def lyr_not_vis(df_zoom):
    for lyr in df_zoom:
        if lyr.isGroupLayer == True:
            lyr_g = arcpy.mapping.ListLayers(lyr)
            for lyr_in_g in lyr_g:
                lyr_in_g.visible = False
                del lyr_in_g, lyr_g
        else:
            lyr.visble = False
        del lyr
    arcpy.RefreshTOC()
