
#-------------------------------------------------------------------------------
# Name:        ClassifySelfIntersectingPolylines
# Purpose:
#
# Author:      geor7025
#
# Created:     23/02/2016
# Copyright:   (c) Esri 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


# import statements
import arcpy
import os

# common variables
py = "PYTHON_9.3"
convexity_area_ratio_threshold = 20
straight_deviation = 3


def main():
    # other prep statements
    arcpy.env.overwriteOutput = True

    # input parameters
    fc = arcpy.GetParameterAsText(0)
    route_id_fld = arcpy.GetParameterAsText(1)
    output_gdb = arcpy.GetParameterAsText(2)

    AnalyzePolylines(fc, route_id_fld, output_gdb)


def AnalyzePolylines(fc, route_id_fld, output_gdb):
    
    fc_name = os.path.basename(fc)
    if fc_name[-4:] == ".shp":
        fc_name = fc_name[:-4]
    fc_F2L = os.path.join(output_gdb, fc_name + "_F2L")
    fc_Diss = os.path.join(output_gdb, fc_name + "_SelfIntClassification")
    
    arcpy.AddMessage("Executing Feature To Line...")
    arcpy.FeatureToLine_management(fc, fc_F2L)
    arcpy.AddMessage("Executing Dissolve...")
    arcpy.Dissolve_management(fc_F2L, fc_Diss, route_id_fld)
    
    arcpy.AddField_management(fc_Diss, "SelfIntersectionType", "TEXT", "", "", 50)
    
    arcpy.AddMessage("Classifying routes...")
    with arcpy.da.UpdateCursor(fc_Diss, ["SHAPE@", "SelfIntersectionType", route_id_fld]) as uCursor:
        
        for i, row in enumerate(uCursor):
            intersection_tuples_dict = {}   # Keeps track of the number of times a particular vertex has come up for a route
            vtx_list = []  # Running list of vertices
            if i % 1000 == 0 and i != 0:
                arcpy.AddMessage("      Number of routes classified: " + str(i))
            partnum = 0
            #if row[1].isMultipart:
            
            vtx_prev = None
            skip_feature = False
                 
            for part in row[0]:
                vtx_list.append([])
                # Step through each vertex in the feature
                vtx_prev = None
                for vtx in part:
                    vtx_current = (vtx.X, vtx.Y)
                        
                    # first check if the current vertex is already in intersection_tuples_dict.
                    # If it's just a matter of duplicate consecutive vertices in this part, ignore (2nd clause in if statement condition)
                    if vtx_current in intersection_tuples_dict and vtx_prev != vtx_current:
                        if partnum in intersection_tuples_dict[vtx_current]:
                            intersection_tuples_dict[vtx_current][partnum] += 1
                        else:
                            intersection_tuples_dict[vtx_current][partnum] = 1
                            
                    # if the current vertex is not already in intersection_tuples_dict, we still need to check if it's among
                    # the vertices already reviewed (i.e., those in vtx_list)
                    else:
                        if vtx_prev != vtx_current:   # want to ignore duplicate consecutive vertices
                            
                            vtx_in_list = False
                            vtx_part = None

                            for i, ls in enumerate(vtx_list):
                                if vtx_current in ls:
                                    vtx_part = i
                                    vtx_in_list = True
                                    
                            # if vtx_current is in the list, and it's part is the same as the previous incidence's:
                            if vtx_in_list and partnum == vtx_part:
                                intersection_tuples_dict[vtx_current] = {partnum: 2}
                            
                            # if vtx_current is in the list, but it's not from the same part as the previous incidence's, add it's part to the dictionary with a count of 1    
                            elif vtx_in_list:
                                intersection_tuples_dict[vtx_current] = {vtx_part: 1}
                                intersection_tuples_dict[vtx_current][partnum] = 1
                            
                    
                    # Add the vertex to the current part's list
                    if vtx_prev != vtx_current:
                        vtx_list[partnum].append(vtx_current)
                            
                    # save the current vertex as vtx_prev for the next iteration        
                    vtx_prev = vtx_current
                    
                    # if the feature has over 100k vertices, it may cause the tool to crash.  Quick reviewing this vertex and put a warning.
                    if len(vtx_list)> 100000:
                        arcpy.AddWarning("Route " + row[2] + " has more than 100,000 vertices.  Analyze manually.")
                        skip_feature = True  # added in order to break out of the outer for loop
                        continue
                if skip_feature:
                    continue
    
                partnum += 1
            
            
            # Categorize the route based on the intersection info collected
            category = "Not self-intersecting"
            
            # More than two intersection points found
            if len(intersection_tuples_dict) >= 3:
                leng = len(intersection_tuples_dict)
                category = "Complex: " + str(leng) + " intersections total"
            
            # Only one intersection point found
            elif len(intersection_tuples_dict) == 1:
                for point_key in intersection_tuples_dict:
                    
                    if len(intersection_tuples_dict[point_key]) == 1:
                        category = "Loop"
                    elif len(intersection_tuples_dict[point_key]) == 2:
                        part_pt_counts = []
                        for key in intersection_tuples_dict[point_key]:
                            part_pt_counts.append(intersection_tuples_dict[point_key][key])
                        part_pt_counts.sort()
                        if part_pt_counts == [2,2]:
                            category = "Infinity" 
                        else:
                            category = "Lollipop"
                    elif len(intersection_tuples_dict[point_key]) == 3:
                        part_pt_counts = []
                        for key in intersection_tuples_dict[point_key]:
                            part_pt_counts.append(intersection_tuples_dict[point_key][key])
                        part_pt_counts.sort()
                        if part_pt_counts == [1,1,2]:
                            category = "Alpha" 
                        else:
                            category = "Branch"
                    else:
                        length = len(intersection_tuples_dict[point_key])
                        category = "Single self-intersection with " + str(length) + " approaches"
            # Two intersection points found
            elif len(intersection_tuples_dict) == 2:
                    
                category_int1 = None
                category_int2 = None
                        
                # Retrieve key for each intersection
                key_list = []
                for key in intersection_tuples_dict:
                    key_list.append(key)
                        
                # Classify the first intersection    
                for partnum_key in intersection_tuples_dict[key_list[0]]:
                    if intersection_tuples_dict[key_list[0]][partnum_key] == 2:
                        category_int1 = "Lollipop"
                if not category_int1:
                    category_int1 = "Branch"
                if len(intersection_tuples_dict[key_list[0]]) > 2:
                    category_int1 = "Branch or Alpha"
                        
                # Classify the second intersection        
                for partnum_key in intersection_tuples_dict[key_list[1]]:
                    if intersection_tuples_dict[key_list[1]][partnum_key] == 2:
                        category_int2 = "Lollipop"
                if not category_int2:
                    category_int2 = "Branch"
                if len(intersection_tuples_dict[key_list[1]]) > 2:
                    category_int1 = "Branch or Alpha"
                      
                # Classify the route based on the two intersections        
                if category_int1 == "Lollipop" and category_int2 == "Lollipop":
                    category = "Barbell"
                else:
                    int_ct = len(intersection_tuples_dict)
                    category = "Complex: 2 intersections total"

            row[1] = category

            uCursor.updateRow(row)
                
    arcpy.Delete_management(fc_F2L)

    stats_table = os.path.join(output_gdb, "SelfIntersectingRoutes_CategoryCounts")
    arcpy.Statistics_analysis(fc_Diss, stats_table, [["Shape_Length", "SUM"]], "SelfIntersectionType")

if __name__ == '__main__':
    main()
