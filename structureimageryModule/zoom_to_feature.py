from arcpy import panToExtent, getSelectedExtent, RefreshTOC, RefreshActiveView
def zoom_to_feature(df_zoom, add_lyr)
    df_zoom.panToExtent(add_lyr.getSelectedExtent())
    add_lyr.visible = True
    RefreshTOC()
    RefreshActiveView()



