#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      chrism
#
# Created:     19/12/2020
# Copyright:   (c) chrism 2020
# License:     <your license>
# 
#-------------------------------------------------------------------------------
import arcpy
import os, sys, xlwt
import xlrd
from xlrd import open_workbook

class aSurvey:
#table_fields = [u'OBJECTID', u'SHAPE', u'pid', u'pname', u'linear_measure_ft', u'lateral_measure_ft', u'side', u'obj_type', u'dimensions_in', u'survey_method', u'survey_date', u'survey_by_name']

    def __init__(self,s_data):
        ##[lateral_measure_ft,linear_measure_ft,lateral_x,linear_y,side,obj_id,obj_type,obj_name,dimensions_in,survey_method,survey_date,survey_by_name]
        if s_data[5] == '' or type(s_data[5]) == 'unicode':
            self.pid = 0
        else:
            self.pid                = s_data[5] ## pid
        self.pname              = s_data[7] ## pname
        self.obj_type           = s_data[6] ## obj_type
        self.linear_measure_ft  = s_data[1] ## linear_measure_ft y-axis
        self.lateral_measure_ft = s_data[0] ## lateral_measure_ft x-axis
        self.side               = s_data[4] ## side
        self.dimensions_in      = s_data[8]
        self.survey_method      = s_data[9]
        self.survey_date        = s_data[10]
        self.survey_by_name     = s_data[11]
        self.point              = arcpy.Point(s_data[2],s_data[3])
        self.SHAPE              = arcpy.PointGeometry(self.point) ## SHAPE

def adjCoord(origin_x, xmeas, origin_y, ymeas,side):
    if side == 'L':
        x_res = origin_x - xmeas
    else:
        x_res = origin_x + xmeas
    y_res = origin_y + ymeas
    return x_res, y_res

#
# import data for formatted Excel worksheet
# 
# columns:
# Linear Measure (ft),Lateral Measure (ft),Side,ID,ObjType	Object,Dimensions,Survey Method,survey_date,survey_by_name
# the data is collected using "baseline measuring" where a 100' tape measure was stretched across the cemetery and then
# feature data was collected by recording the linear measure on the tape measure, then a perpendicular measure from the
# tape measure to the feature (Lateral Measure). The "Side" field collects the direction of the lateral measure. 
# The rest of the columns are attributes that describe the feature at the determined location (i.e., can be changed in
# output schema to match the data collected).
input_book = arcpy.GetParameterAsText(0)
if not input_book or input_book == '':
    input_book = r"H:\Cmac\Geneaology\Studies and Projects\07_cemetery_surveys\Survey_March2019.xlsx"

origin_x = arcpy.GetParameter(1)
if not origin_x or origin_x == '':
    origin_x = 1243912.568

origin_y = arcpy.GetParameter(2)
if not origin_y or origin_y == '':
    origin_y = 928660.376

sr = arcpy.GetParameter(3)    # Spatial Reference (NC State Plane). 
if not sr or sr == '':
    sr = arcpy.SpatialReference(2264)

output_fc = arcpy.GetParameter(4)
if not output_fc or output_fc == '':
    output_fc = r"H:\Cmac\Geneaology\Studies and Projects\07_cemetery_surveys\site_data.gdb\survey_points"

arcpy.env.workspace = os.path.dirname(output_fc)
arcpy.SpatialReference = sr

# READ
book = open_workbook(filename=input_book)
survey_data = []

for name in book.sheet_names():
    # choose a sheet to read
    if name == 'Data':
        sheet = book.sheet_by_name(name)

    rowindex = 0
    # optionally, find header row
    # find the header column by searching for a known column header
    search_hdr_result = [sheet.row(row)[0].value for row in range(sheet.nrows)]
    rowindex = search_hdr_result.index("Linear Measure (ft)")
    # skip header row to start collecting data
    skip_header_row = rowindex + 1

    # read data
    while rowindex < sheet.nrows:
        cells = sheet.row(rowindex)
        row = []
        b = []

        # test/validate data as necessary
        if rowindex >= skip_header_row and cells[0].value != "" and cells[1].value != "" and cells[2].value != "":

            linear_measure_ft       = sheet.row(rowindex)[0].value
            lateral_measure_ft      = sheet.row(rowindex)[1].value
            side                    = sheet.row(rowindex)[2].value
            obj_id                  = sheet.row(rowindex)[3].value
            obj_type                = sheet.row(rowindex)[4].value
            obj_name                = sheet.row(rowindex)[5].value
            dimensions_in           = sheet.row(rowindex)[6].value
            survey_method           = sheet.row(rowindex)[7].value
            survey_date             = sheet.row(rowindex)[8].value
            survey_by_name          = sheet.row(rowindex)[9].value

            # print the result
            print('{},{},{},{},{},{},{}'.format(linear_measure_ft,lateral_measure_ft,side,obj_id,obj_type,obj_name,dimensions_in,survey_method,survey_date,survey_by_name))


            # Adjust from the origin coordinates to derive a state plane coordinate.
            lateral_x,linear_y = adjCoord(origin_x,lateral_measure_ft, origin_y, linear_measure_ft,side)
            print('{},{},{},{},{},{}'.format(lateral_x,linear_y,side,obj_id,obj_type,obj_name,dimensions_in))
            survey_data.append(aSurvey([lateral_measure_ft,linear_measure_ft,lateral_x,linear_y,side,obj_id,obj_type,obj_name,dimensions_in,survey_method,survey_date,survey_by_name]))

        rowindex += 1

table_fields = ['SHAPE', 'pid', 'pname', 'linear_measure_ft', 'lateral_measure_ft', 'side', 'obj_type', 'dimensions_in', 'survey_method', 'survey_date', 'survey_by_name']

with arcpy.da.Editor(arcpy.env.workspace) as edit:
    cursor = arcpy.da.InsertCursor(output_fc,table_fields)
    for survey in survey_data:
        row_data = [survey.SHAPE, survey.pid, survey.pname, survey.linear_measure_ft, survey.lateral_measure_ft, survey.side, survey.obj_type, survey.dimensions_in, survey.survey_method, survey.survey_date, survey.survey_by_name]
        print(row_data)
        cursor.insertRow(row_data)

del cursor
