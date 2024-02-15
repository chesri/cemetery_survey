# cemetery_survey

In development - tool is somewhat hard-coded now and is designed to work with Esri arcpy module and requires a license for ArcGIS Pro 3.x.

Tools for collecting baseline measure survey data and converting it to points.

The python script in this repo simply reads formatted data from a spreadsheet containing observed measurements for a survey (a cemetery in this context). The measurements are collected in two dimensions: linear and lateral.

The data is collected using "baseline measuring" where a 100' tape measure was stretched across the cemetery and then feature data was collected by recording the linear measure on the tape measure and then a perpendicular (lateral) measure from the tape measure to the feature . There is a "side" field that records the direction of the lateral measure. The rest of the columns are attributes that describe the feature at the determined location (i.e., can be changed in output schema to match the data collected).

Spreadsheet format:

| Column Header        | Purpose                                                                                                                                  | Example Data                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Linear Measure (ft)  | measure along the baseline                                                                                                               | 12.5                                                  |
| Lateral Measure (ft) | measure from baseline                                                                                                                    | 20.8                                                  |
| Side                 | "R" or "L" side of baseline                                                                                                              | R                                                     |
| ID                   | Identification value                                                                                                                     | 1                                                     |
| ObjType              | one word description of point feature                                                                                                    | headstone                                             |
| Point Name (pname)   | descriptive name of feature                                                                                                              | HS: Maggie Greer, b. July 5, 1879, d. August 24, 1950 |
| Dimensions           | dimensions of feature                                                                                                                    | 45"x22"                                               |
| Survey Method        | record how the point was derived since it will be in database with other points that could have been derived by other means (e.g., GPS). | baseline measuring                                    |
| survey_date          | date the point was collected                                                                                                             | 3/16/2019                                             |
| survey_by_name       | who collected the point                                                                                                                  | Chris McGuire                                         |
