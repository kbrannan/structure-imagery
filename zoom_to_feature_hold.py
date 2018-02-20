import arcpy, os                                        # arcpy provides useful way to perform map automation, os provides tools to deal with filenames, paths, directories

# Search for specific table and field (unique values), then return a sorted list from given iterable
def unique_values(table , field):
    with arcpy.da.SearchCursor(table, field) as cursor:         # search for unique value, what does "as cursor" do?
        return sorted({row[0] for row in cursor})               # return a sorted list of 1st row, what does "in cursor" mean?

# Why is there an r' in front of each literal?  (I know it tells Python to disregard any special characters . . . )
str_path_mxd = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\MapDocs'     # Create file path for .mxd files
str_file_mxd = r'Upper Yaquina Near-Stream Structures (scratch).mxd'                            # Create name for .mxd file
str_df_zoom_name = r'Zoom to Feature'                                                           # Create variable name for selected feature to zoom to extent to
str_df_state_name = r'Overall Watershed'                                                        # Create variable name for Watershed
str_strc_cent = r'PointPotentialStructureCentroids'                                             # Create variable for a point that is the center of the structure
str_strc_poly = r'Potential Structures'                                                         # Create a variable for potential structures
str_strm_line = r'NHD Flowlines'                                                                # Create variable for National Hydrography Dataset flowlines

str_path_export = r'\\deqhq1\tmdl\tmdl_wr\midcoast\GIS\BacteriaTMDL\UpperYaquinaRiver\python\structure-imagery\images'      # Create path for structure images to be exported to
str_file_image_export_prefix = 'strt_'                                                                                      # Create variable for image export prefix


# Return .mxd files specified by path
if os.path.isfile(str_path_mxd + "\\" + str_file_mxd):
    mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)                     # Create variable for current .mxd file to make changes to
    df_zoom = arcpy.mapping.ListDataFrames(mxd_cur, str_df_zoom_name)[0]                        # Variable created, will Search for first data frame in.mxd file above, will it search for the zoom to extent of the structures?
    df_state = arcpy.mapping.ListDataFrames(mxd_cur, str_df_state_name)[0]                      # Variable created, will search for overall watershed from the first data frame in the .mxd file
    #mxd_cur.activeView='PAGE_LAYOUT' # make sure the page layout is current view to get map with mulp data frames
    #mxd_cur.save() # have to save and then reload mxd for the change in active view to take effect
    #del mxd_cur
    #mxd_cur = arcpy.mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)

SelLayer = arcpy.mapping.ListLayers(mxd_cur, str_strc_poly, df_zoom)[0]       # Variable created that will return a list of potential structures, zoom to extent, from the .mxd file

mylist = unique_values(SelLayer,'FID')                                        # What does this line do? What is FID?

# make all layers not visible
for lyr in df_zoom:
    if lyr.isGroupLayer == True:
        #print "Layers in " + lyr.name
        lyr_g = arcpy.mapping.ListLayers(lyr)
        for lyr_in_g in lyr_g:
            #print lyr_in_g.name
            lyr_in_g.visible = False
        #print ""
        del lyr_in_g, lyr_g
    else:
        print lyr.name
        lyr.visble = False
lyr = arcpy.mapping.ListLayers(mxd_cur, str_strm_line, df_zoom)[0]             # layer Variable created that will return a list of zoomed in extent of NHD Flowlines from the first data frame from the .mxd file?
lyr.visible = True                                                             # make this variable visible
del lyr                                                                        # delete the layer variable
arcpy.RefreshTOC()

memSelLyr = "in_memory" + "\\" + "memSelLayer"

# Based on attribute query features are extracted from "SelLayer" and a new layer "memSelLyr" is the output created, which is then
# added to the top of the data frame, this new layer replaces previous "SelLayer". This layer is made visible, .mxd file is then exported to a .png file,
# once exported the new layer is deleted
for curFID in mylist:
    query = '"FID" = {}'.format(curFID)
    # Process: Select
    arcpy.Select_analysis(SelLayer, memSelLyr, query)                          # Extract features from "SelLayer", output feature class "memSelLyr" is created
    add_lyr = arcpy.mapping.Layer(memSelLyr)                                   # Variable references "memSellyr" layer
    arcpy.mapping.AddLayer(df_zoom, add_lyr, "TOP")                                                                                 # Add layer to top of data frame
    arcpy.SelectLayerByAttribute_management(in_layer_or_view=add_lyr, selection_type='NEW_SELECTION', where_clause=query)           # Replace current selection with memSellyr, query is subset of records selected
    df_zoom.panToExtent(add_lyr.getSelectedExtent())
    #df.zoomToSelectedFeatures()
    add_lyr.visible = True
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    arcpy.mapping.ExportToPNG(map_document=mxd_cur, out_png=str_path_export + '\\' + str_file_image_export_prefix +'{}'.format(curFID) + '_ext_pg.png')
    arcpy.Delete_management(add_lyr)
    arcpy.Delete_management("in_memory")                                       # What is "in_memory"?
    del query


