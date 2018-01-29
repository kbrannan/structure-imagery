import arcpy.da

def unique_values(table , field):
    with arcpy.da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})
