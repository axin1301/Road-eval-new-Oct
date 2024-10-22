#111598 111872 80868 81134
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
# 增加最大图像大小限制
Image.MAX_IMAGE_PIXELS = None
import math
import json
from tqdm import tqdm
import pandas as pd
# 读取文件并提取特定行的值
def get_values_from_file(filename, target_image):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(target_image):
                values = line.split(':')[1].strip().split()
                return {
                    "Left_Edge_Longitude": float(values[0]),
                    "Right_Edge_Longitude": float(values[1]),
                    "Top_Edge_Latitude": float(values[2]),
                    "Bottom_Edge_Latitude": float(values[3])
                }
    return None

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
# 文件名
import os
# 定义函数来提取第二个和第三个数值
def extract_numbers(img_name):
    parts = img_name.split('_')
    second_number = int(parts[1])
    third_number = int(parts[2])
    return second_number, third_number

# district_list = ['340827']#['141034']#['341203']
# district_list = ['130125', '130126', '130129', '130425', '130434', '130522', '130529', '130530', '130531', '130532', '130533', \
#                         '130631', '130634', '130636', '130708', '130924', '130925', '130927', '131122', '131123', '131124', '131128', \
#                             '140223', '140427', '140829', '140931', '141030', '141034', '340827', '341203']#


def transform_coord_grid(district,year):
# district_list = ['130522', '610328', '130533', '130529', '130532', '130531', '130631', '131123', '131122', '141034', '130925', '131128', '341203', '131124', '130434', '522635']
# ['500241', '610329', '141034', '341203', '360724', '360781', '522635', '341523', '130636', '360830', '520328', '520327', '610826', '450123', '411324', '130425', '430822', '411625', '130925', '610426', '532324', '130434', '540229', '411523', '360321', '130924', '530827', '410327', '522327', '130522', '622901', '431228', '530829', '630203', '431028', '621125', '430821', '131123', '130125', '513437', '620523', '610929', '433123', '410927', '140723', '140931', '130708', '140427', '130927', '622923', '522326', '610926', '141126', '130727', '451022', '131128', '610430', '469024', '130529', '532325', '620102', '360821', '530624', '520424', '469030', '610222', '410225', '530923', '513322', '533301', '620802', '410328', '610729', '431225', '430225', '341322', '130731', '130533', '130126', '520326', '340828', '511529', '522729', '140927', '522632', '360726', '510824', '451121', '433130', '530521', '140223', '522325', '130630', '530629', '610727', '620821', '511602', '450329', '140929', '610831', '532925', '540502', '520624', '630225', '130531', '469001', '610328', '140224', '530924', '520425', '532932', '610527', '511381', '620525', '140221', '522623', '513435', '420529', '140429', '141030', '431027', '131124', '520324', '340826', '431230', '130624', '140928', '422827', '532523', '131122', '620122', '450125', '411422', '532931', '520403', '130129', '410325', '130631', '520525', '520203', '130728', '430529', '340827', '610924', '533122', '141028', '522634', '411723', '140829', '451027', '130530', '361125', '610722', '141127', '360828', '422823', '640402', '532601', '130709', '522628', '610927', '141129', '540104', '411321', '520628', '513338', '140215', '140425', '510525', '540123', '130532', '130634']
    year_list = [year]
    district_list = [district]
    # district_list_reverse = district_list[::-1]

    if not os.path.exists('results_pixel_coored_final_wgs_test/'):
        os.makedirs('results_pixel_coored_final_wgs_test/')
    for district in district_list:#_reverse:
        for year in year_list:
            if os.path.exists('results_pixel_coored_final_wgs_test/'+district+'_'+str(year)+'-GE-18-final-wgs.json'):
                break

            # filename = '../../../GE_image_zip_'+str(year)+'/'+district+'/'+str(year)+'/'+district+'_list1.txt'

            file_C = 'results_pixel_bone_pred_test/results_pixel_bone_pred_'+district+'_'+str(year)+'_coord/coord_list_simplified.txt'
            # if os.path.exists('results_pixel_coored_final_wgs/'+district+'_'+str(year)+'-GE-18-final-wgs.json'):
            #     continue
            if not os.path.exists(file_C):
                continue
            data_C = read_points_from_file_C(file_C)
            print(len(data_C))
            cnt=0
            coordinates = []
            bar = tqdm(range(len(data_C)))
            
            csv_file_path = '../data_test/tilefile_zl16_20_plus_20/'+ district+'.csv'#################################
            # csv_file_path = '../../../GE_image_zip_2020/image_list_file/'+district+'_invalid_tile_'+str(year)+'.csv'  # 请将此路径替换为你的CSV文件路径
            df = pd.read_csv(csv_file_path)
            min_x = df['x_tile'].min()
            max_x = df['x_tile'].max()
            min_y = df['y_tile'].min()
            max_y = df['y_tile'].max()
            # 应用函数来创建新的列
            # df[['second_number', 'third_number']] = df['img_name'].apply(lambda x: pd.Series(extract_numbers(x)))
            # min_x = df['second_number'].min()
            # max_y = df['third_number'].max()

            # print(min_x, max_y)  ###124,133

            # skeleton = Image.open('../../test_run/skeleton_file_final_d300/pred_skeleton_'+district+'_'+str(year)+'_2_improve.png')
            skeleton = Image.open('../temp_output_test/'+district+'_GT_primary_'+str(year)+'-17-bone.png')
            
            skeleton = np.array(skeleton)

            x_shape,y_shape = skeleton.shape[0],skeleton.shape[1]
            print(x_shape,y_shape)

            for i in bar:
                # print(data_C[i])
                (x,y) = data_C[i][0]
                # print(x,y)
                x = min(x,y_shape)
                y = min(y,x_shape)
                print(x,y)

                row_img_num = math.floor((y)/128)  ####因为inference结果 resize到128了
                row_img_delta = y%128#################y
                col_img_num = math.floor((x)/128)
                col_img_delta = x%128  ########x
                # print(row_img_num,row_img_delta,col_img_num,col_img_delta)
            

                # # 获取第二个数值的最小值和第三个数值的最大值
                # second_min = df['second_number'].min()
                # third_max = df['third_number'].max()
                # img_x = 111598 + col_img_num
                # img_y = 81135 - row_img_num

                img_x = min_x + col_img_num
                img_y = min_y + row_img_num 
                # img_y = max_y  - row_img_num

                # 目标图片名
                target_image = str(img_y)+'_'+str(img_x) #+ '.png'
                # target_image = 'gesh_'+str(img_x)+'_'+str(img_y)+'_18.jpg'

                df_tmp = df[df['img_name']==target_image]
                print(df_tmp)
                pixel_lat = df_tmp["Top_Edge_Latitude"].values-(df_tmp["Top_Edge_Latitude"].values-df_tmp["Bottom_Edge_Latitude"].values)/128*row_img_delta
                pixel_lng = (df_tmp["Right_Edge_Longitude"].values-df_tmp["Left_Edge_Longitude"].values)/128*col_img_delta+df_tmp["Left_Edge_Longitude"].values
                print(pixel_lat,pixel_lng)

                # # 获取并打印值
                # values = get_values_from_file(filename, target_image)
                # if values is None:
                #     coordinates.append([-1,-1])
                #     continue
                #     # continue
                # #print(target_image,values,x,y,col_img_num,row_img_num)
                # # if values:
                # #     print("Left_Edge_Longitude:", values["Left_Edge_Longitude"])
                # #     print("Right_Edge_Longitude:", values["Right_Edge_Longitude"])
                # #     print("Top_Edge_Latitude:", values["Top_Edge_Latitude"])
                # #     print("Bottom_Edge_Latitude:", values["Bottom_Edge_Latitude"])
                # # else:
                # #     print("未找到目标图片的信息。")
                # #     cnt+=1
                
                # pixel_lat = values["Top_Edge_Latitude"]-(values["Top_Edge_Latitude"]-values["Bottom_Edge_Latitude"])/128*row_img_delta
                # pixel_lng = (values["Right_Edge_Longitude"]-values["Left_Edge_Longitude"])/128*col_img_delta+values["Left_Edge_Longitude"]
                # print(pixel_lat,pixel_lng)
                coordinates.append([pixel_lat[0],pixel_lng[0]])
                
            # if values is None:
            #     continue
            # 将坐标转换为所需的格式 [[[lon, lat]], [[lon, lat]]]
            formatted_coordinates = [[ll] for ll in coordinates]
            print(formatted_coordinates)

            # 将结果写入JSON文件
            output_file = 'results_pixel_coored_final_wgs_test/'+district+'_'+str(year)+'-GE-18-final-wgs.json'
            with open(output_file, 'w') as file:
                json.dump(formatted_coordinates, file, indent=4)
            # print(cnt)
# transform_coord_grid('130634',2020)