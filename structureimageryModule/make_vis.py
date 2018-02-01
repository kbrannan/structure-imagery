from arcpy import mapping, Delete_management, RefreshTOC, RefreshActiveView

def make_vis(mxd_cur, df, listlyr):
    for str_lyr in listlyr:
        lyr_cur = mapping.ListLayers(mxd_cur, str_lyr, df)[0]
        lyr_cur.visible = True
        Delete_management(lyr_cur)
    RefreshTOC()
    RefreshActiveView()
