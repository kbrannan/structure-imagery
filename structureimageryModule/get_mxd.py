from os import path
from arcpy import mapping

def get_mxd(str_path_mxd, str_file_mxd):
    if path.isfile(str_path_mxd + "\\" + str_file_mxd):
        mxd_cur = mapping.MapDocument(str_path_mxd + "\\" + str_file_mxd)
