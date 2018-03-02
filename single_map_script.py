import structureimagery as strimage


str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'
str_file_mxd = r'UY_NSS_scratch.mxd'
str_df_zoom_name = r'Zoom to Feature'
str_df_state_name = r'Overall Watershed'
str_strc_cent = r'PointPotentialStructureCentroids'
str_strc_poly = r'Potential Structures'
str_strm_line = r'NHD Flowlines'
str_mxd_save_post = r".mxd"                     #BRC added

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'
str_file_image_export_prefix = 'strt_'
mxd = (str_path_mxd + "\\" + str_file_mxd)  #BRC added (simplify the process?)
mxd_cur = arcpy.mapping.MapDocument(mxd)     #BRC added
curFID = 36


#mxd_cur = strimage.get_mxd(str_path_mxd, str_file_mxd)     #BRC simplified getting .mxd

df_zoom = strimage.get_df(mxd_cur, str_df_zoom_name)

sel_lyr = strimage.get_sel_layer(mxd_cur, str_strc_cent, df_zoom)

#strimage.make_not_vis(df_zoom)

strimage.make_vis(mxd_cur, df_zoom, [str_strc_poly, str_strm_line])

strimage.gen_map_image(curFID, sel_lyr, df_zoom, mxd_cur, str_path_export, str_file_image_export_prefix)
