from scipy.interpolate import interp1d
import json
import numpy as np
import matplotlib.pyplot as plt
from simplification.cutil import (
    simplify_coords,
    simplify_coords_idx,
    simplify_coords_vw,
    simplify_coords_vw_idx,
    simplify_coords_vwp,
)
import os
# # Using Ramer–Douglas–Peucker
# coords = [
#     [0.0, 0.0],
#     [5.0, 4.0],
#     [11.0, 5.5],
#     [17.3, 3.2],
#     [27.8, 0.1]
# ]

# # For RDP, Try an epsilon of 1.0 to start with. Other sensible values include 0.01, 0.001
# simplified = simplify_coords(coords, 1.0)
# print(simplified)

# 读取文本文件 C 中的数据，格式为行列号
def read_points_from_file_C(file_path):
    points = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            coords = list(map(int, line.strip().split()))
            points.append([(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)])
    print(len(points))
    return points

# district_list = ['340827']#['141034']#['341203']
# district_list = ['130125', '130126', '130129', '130425', '130434', '130522', '130529', '130530', '130531', '130532', '130533', \
#                         '130631', '130634', '130636', '130708', '130924', '130925', '130927', '131122', '131123', '131124', '131128', \
#                             '140223', '140427', '140829', '140931', '141030', '141034', '340827', '341203']#

def simplify_road(district,year):
    district_list = [district]
# district_list = ['520603', '130522', '469024', '522636', '469029', '410225', '610328', '522630', '620102', '620102', '130533', '420921', '411423', '130529', '130532', '630203', '130531', '622924', '130631', '411424', '361125', '131123', '131122', '141034', '610430', '540524', '130925', '411422', '520602', '411327', '622927', '530626', '433124', '610428', '131128', '341203', '131124', '130434', '522635']
# ['130631', '131123', '131122', '141034', '130925', '131128', '341203', '131124', '130434', '522635']# ['610328', '130533', '130529', '130532', '130531']#['130522']#['500241', '610329', '141034', '341203', '360724', '360781', '522635', '341523', '130636', '360830', '520328', '520327', '610826', '450123', '411324', '130425', '430822', '411625', '130925', '610426', '532324', '130434', '540229', '411523', '360321', '130924', '530827', '410327', '522327', '130522', '622901', '431228', '530829', '630203', '431028', '621125', '430821', '131123', '130125', '513437', '620523', '610929', '433123', '410927', '140723', '140931', '130708', '140427', '130927', '622923', '522326', '610926', '141126', '130727', '451022', '131128', '610430', '469024', '130529', '532325', '620102', '360821', '530624', '520424', '469030', '610222', '410225', '530923', '513322', '533301', '620802', '410328', '610729', '431225', '430225', '341322', '130731', '130533', '130126', '520326', '340828', '511529', '522729', '140927', '522632', '360726', '510824', '451121', '433130', '530521', '140223', '522325', '130630', '530629', '610727', '620821', '511602', '450329', '140929', '610831', '532925', '540502', '520624', '630225', '130531', '469001', '610328', '140224', '530924', '520425', '532932', '610527', '511381', '620525', '140221', '522623', '513435', '420529', '140429', '141030', '431027', '131124', '520324', '340826', '431230', '130624', '140928', '422827', '532523', '131122', '620122', '450125', '411422', '532931', '520403', '130129', '410325', '130631', '520525', '520203', '130728', '430529', '340827', '610924', '533122', '141028', '522634', '411723', '140829', '451027', '130530', '361125', '610722', '141127', '360828', '422823', '640402', '532601', '130709', '522628', '610927', '141129', '540104', '411321', '520628', '513338', '140215', '140425', '510525', '540123', '130532', '130634']

    year_list = [2020]

    for district in district_list:
        for year in year_list:

            # file_C = 'coord_list_bone.txt'
            file_C = 'results_pixel_bone_pred/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/coord_list.txt' #'coord_list.txt'
            if not os.path.exists(file_C):
                continue
            points_C = read_points_from_file_C(file_C)
            # print(points_C[0])

            simplified_points = []
            for i in range(len(points_C)):
                data = points_C[i]
                simplified = simplify_coords(data, 1.0)
                simplified_points.append(simplified)
            print(simplified_points)
            data = simplified_points


            # 写入第一份文件
            os.makedirs('results_pixel_bone_pred/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/', exist_ok=True)
            with open('results_pixel_bone_pred/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/coord_list_simplified.txt', 'w') as f:
                for sublist in data:
                    for coord in sublist:
                        # print(coord)
                        f.write(f"{int(coord[0])} {int(coord[1])}\n")

            # print("第一份文件写入完成：output1.txt")

            # 写入第二份文件
            with open('results_pixel_bone_pred/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/coord_list_simplified_edge.txt', 'w') as f:
                for sublist in data:
                    line = " ".join([f"{int(coord[0])} {int(coord[1])}" for coord in sublist])
                    f.write(f"{line}\n")

            os.makedirs('results_pixel_bone_pred/pixel/', exist_ok=True)
            with open('results_pixel_bone_pred/pixel/'+district+'-'+str(17)+'-simplified.txt', 'w') as f:
                for sublist in data:
                    line = " ".join([f"{int(coord[0])} {int(coord[1])}" for coord in sublist])
                    f.write(f"{line}\n")

# print("第二份文件写入完成：output2.txt")
# data = points_C #[0]

# print(data)

# for data in points_C:
#     x_values = [point[0] for point in data]
#     y_values = [point[1] for point in data]

#     # 创建图形并绘制线条
#     plt.plot(x_values, y_values, marker='o',color = 'b')

# fig, ax = plt.subplots()

# for data in points_C:
#     x_values = [point[0] for point in data]
#     y_values = [point[1] for point in data]
# # 绘制数据点
#     ax.plot(x_values, y_values, marker='o',color = 'b')

# for data in simplified_points:
#     x_values = [point[0] for point in data]
#     y_values = [point[1] for point in data]
# # 绘制数据点
#     ax.plot(x_values, y_values, marker='*',color = 'r')

# # 设置比例尺相同
# ax.set_aspect('equal')
# # 将 (0, 0) 点放在左上角
# ax.invert_yaxis()
# # 添加标题和标签
# ax.set_title('Equal Aspect Ratio Plot')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')

# # for data in simplified_points:
# #     x_values = [point[0] for point in data]
# #     y_values = [point[1] for point in data]

# #     # 创建图形并绘制线条
# #     plt.plot(x_values, y_values, marker='x',color = 'r')
# # # 添加标题和标签
# # plt.title('Line Plot of Given Data')
# # plt.xlabel('X-axis')
# # plt.ylabel('Y-axis')
# # plt.set_aspect('equal', 'box')
# # 显示图形
# plt.show()
