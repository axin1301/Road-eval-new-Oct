import geopandas as gpd
import os

def shp2txt_transform_new(district, year):
# for district in ['jingyuxian']:# ['lingqiuxian']: #['xixiangxian','shufuxian','guanghexian','danfengxian','jiangzixian','honghexian','liboxian','linquanxian','jingyuxian','lingqiuxian']:
    # for year in [2021]:
    # for radius in [200]:#[0,50,100,150,200,250,300]:
    # radius = 300 ##只是为了运行方便，并不有300

    if not os.path.exists('../GraphSamplingToolkit-main_improve_GE/'+str(district)+'/xyx_0'+'/groundtruth/'):
        os.makedirs('../GraphSamplingToolkit-main_improve_GE/'+str(district)+'/xyx_0'+'/groundtruth/')
        
    dt_code_city = str(district)[:-2]+str(0)+str(0)
    print(dt_code_city)

    # 读取 SHP 文件
    # shp_file_path = '../../../RoadNetworkValidation_new/RoadNetwork_Validation4OSMGT/data/tdrive_sample_improve2/results_pred_' \
    #                     +district+'_'+str(year) +'/linked_rn_'+str(radius)+'/edges.shp'
    shp_file_path = 'results_pixel_coored_final_shp_test/'+district+'_'+str(year)+'-GE-18-final-wgs_inbound.shp'
    gdf = gpd.read_file(shp_file_path)

    # 选择 polyline 类型的几何对象
    polyline_gdf = gdf[gdf['geometry'].geom_type == 'LineString']

    # 写入点坐标和编号的文本文件
    with open('../GraphSamplingToolkit-main_improve_GE/'+str(district)+'/xyx_0'+'/groundtruth/'+str(district)+'_groundtruth_txt_vertices_osm.txt', 'w') as f_points:
        point_dict = {}  # 用于存储点的经纬度和对应的编号
        point_id = 1
        for index, row in polyline_gdf.iterrows():
            polyline_coords = list(row['geometry'].coords)
            # f_points.write(f"Polyline {index + 1} coordinates:\n")
            for coord in polyline_coords:
                coord_str = f"{coord[0]},{coord[1]}"  # 将经纬度转换为字符串
                if coord_str not in point_dict:
                    point_dict[coord_str] = point_id
                    f_points.write(f"{point_id},{coord[0]},{coord[1]}\n")
                    point_id += 1

    # 判断点之间是否相连，并写入连接关系的文本文件
    with open('../GraphSamplingToolkit-main_improve_GE/'+str(district)+'/xyx_0'+'/groundtruth/'+str(district)+'_groundtruth_txt_edges_osm.txt', 'w') as f_connections:
        line_number = 1  # 行号
        for index, row in polyline_gdf.iterrows():
            polyline_coords = list(row['geometry'].coords)
            for i in range(len(polyline_coords) - 1):
                coord1_str = f"{polyline_coords[i][0]},{polyline_coords[i][1]}"
                coord2_str = f"{polyline_coords[i + 1][0]},{polyline_coords[i + 1][1]}"
                if coord1_str in point_dict and coord2_str in point_dict:
                    point_id1 = point_dict[coord1_str]
                    point_id2 = point_dict[coord2_str]
                    f_connections.write(f"{line_number},{point_id1},{point_id2},1\n")
                    line_number += 1