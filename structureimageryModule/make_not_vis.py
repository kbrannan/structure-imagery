def make_not_vis(df):
    for lyr in df:
        if lyr.isGroupLayer == True:
            for lyr_g in lyr.isGroupLayer:
                lyr_g.visible = False
            del lyr_g
        else:
            lyr.visible = False
