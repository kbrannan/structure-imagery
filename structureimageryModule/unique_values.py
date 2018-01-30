from arcpy import da

def unique_values(table , field):
    with da.SearchCursor(table, field) as cursor:
        return sorted({row[0] for row in cursor})
