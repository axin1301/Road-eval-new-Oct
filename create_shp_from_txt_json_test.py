import geopandas as gpd
from shapely.geometry import LineString
import json

def read_lines_from_txt(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            coords = list(map(int, line.strip().split()))
            points = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            lines.append(LineString(points))
    return lines

def read_points_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    points = [(item[0][1], item[0][0]) for item in data]
    return points

def replace_coords(original_lines, transformed_points):
    new_lines = []
    point_index = 0
    for line in original_lines:
        new_coords = []
        for _ in range(len(line.coords)):
            if point_index < len(transformed_points):
                if transformed_points[point_index] in [(-1, -1)]:
                    point_index += 1
                    continue
                new_coords.append(transformed_points[point_index])
                point_index += 1
        if len(new_coords)<2:
            continue
        new_lines.append(LineString(new_coords))
    return new_lines

import os

def create_shapefile(lines, output_path):
    gdf = gpd.GeoDataFrame(geometry=lines)
    gdf.to_file(output_path, driver='ESRI Shapefile')

# district_list = ['340827']#['141034']#['341203']
# district_list = ['130125', '130126', '130129', '130425', '130434', '130522', '130529', '130530', '130531', '130532', '130533', \
#                         '130631', '130634', '130636', '130708', '130924', '130925', '130927', '131122', '131123', '131124', '131128', \
#                             '140223', '140427', '140829', '140931', '141030', '141034', '340827', '341203']#

def create_shp_from_txt_json(district, year):
    # district_list = ['130522']#, '610328', '130533', '130529', '130532', '130531', '130631', '131123', '131122', '141034', '130925', '131128', '341203', '131124', '130434', '522635']
    # # ['500241', '610329', '141034', '341203', '360724', '360781', '522635', '341523', '130636', '360830', '520328', '520327', '610826', '450123', '411324', '130425', '430822', '411625', '130925', '610426', '532324', '130434', '540229', '411523', '360321', '130924', '530827', '410327', '522327', '130522', '622901', '431228', '530829', '630203', '431028', '621125', '430821', '131123', '130125', '513437', '620523', '610929', '433123', '410927', '140723', '140931', '130708', '140427', '130927', '622923', '522326', '610926', '141126', '130727', '451022', '131128', '610430', '469024', '130529', '532325', '620102', '360821', '530624', '520424', '469030', '610222', '410225', '530923', '513322', '533301', '620802', '410328', '610729', '431225', '430225', '341322', '130731', '130533', '130126', '520326', '340828', '511529', '522729', '140927', '522632', '360726', '510824', '451121', '433130', '530521', '140223', '522325', '130630', '530629', '610727', '620821', '511602', '450329', '140929', '610831', '532925', '540502', '520624', '630225', '130531', '469001', '610328', '140224', '530924', '520425', '532932', '610527', '511381', '620525', '140221', '522623', '513435', '420529', '140429', '141030', '431027', '131124', '520324', '340826', '431230', '130624', '140928', '422827', '532523', '131122', '620122', '450125', '411422', '532931', '520403', '130129', '410325', '130631', '520525', '520203', '130728', '430529', '340827', '610924', '533122', '141028', '522634', '411723', '140829', '451027', '130530', '361125', '610722', '141127', '360828', '422823', '640402', '532601', '130709', '522628', '610927', '141129', '540104', '411321', '520628', '513338', '140215', '140425', '510525', '540123', '130532', '130634']

    # year_list = [2020]

    district_list = [district]
    year_list = [year]
    if not os.path.exists('results_pixel_coored_final_shp_test/'):
        os.makedirs('results_pixel_coored_final_shp_test/')
    for district in district_list:
        for year in year_list:

            # 示例文件路径
            original_file_path = 'results_pixel_bone_pred_test/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/coord_list_simplified_edge.txt' #'output2_GE_jingyuxian.txt'
            transformed_file_path = 'results_pixel_coored_final_wgs_test/'+district+'_'+str(year)+'-GE-18-final-wgs.json' #'jingyuxian-GE-18-final-wgs.json'
            output_path = 'results_pixel_coored_final_shp_test/'+district+'_'+str(year)+'-GE-18-final-wgs.shp'

            if not os.path.exists(original_file_path):
                continue

            if not os.path.exists(transformed_file_path):
                continue

            # if os.path.exists(output_path):
            #     continue
            print(district)
            # 读取原始坐标的LineString
            original_lines = read_lines_from_txt(original_file_path)

            # 读取转换后的坐标点
            transformed_points = read_points_from_json(transformed_file_path)

            if transformed_points is None:
                continue

            # 替换原始坐标为转换后的坐标
            new_lines = replace_coords(original_lines, transformed_points)

            # 创建新的shapefile
            create_shapefile(new_lines, output_path)
