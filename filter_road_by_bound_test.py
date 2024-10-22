import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd
import os

# district_list = ['340827']#['141034']#['341203']
# district_list = ['130125', '130126', '130129', '130425', '130434', '130522', '130529', '130530', '130531', '130532', '130533', \
#                         '130631', '130634', '130636', '130708', '130924', '130925', '130927', '131122', '131123', '131124', '131128', \
#                             '140223', '140427', '140829', '140931', '141030', '141034', '340827', '341203']#

    # district_list = ['130522']#, '610328', '130533', '130529', '130532', '130531', '130631', '131123', '131122', '141034', '130925', '131128', '341203', '131124', '130434', '522635']
    # #['500241', '610329', '141034', '341203', '360724', '360781', '522635', '341523', '130636', '360830', '520328', '520327', '610826', '450123', '411324', '130425', '430822', '411625', '130925', '610426', '532324', '130434', '540229', '411523', '360321', '130924', '530827', '410327', '522327', '130522', '622901', '431228', '530829', '630203', '431028', '621125', '430821', '131123', '130125', '513437', '620523', '610929', '433123', '410927', '140723', '140931', '130708', '140427', '130927', '622923', '522326', '610926', '141126', '130727', '451022', '131128', '610430', '469024', '130529', '532325', '620102', '360821', '530624', '520424', '469030', '610222', '410225', '530923', '513322', '533301', '620802', '410328', '610729', '431225', '430225', '341322', '130731', '130533', '130126', '520326', '340828', '511529', '522729', '140927', '522632', '360726', '510824', '451121', '433130', '530521', '140223', '522325', '130630', '530629', '610727', '620821', '511602', '450329', '140929', '610831', '532925', '540502', '520624', '630225', '130531', '469001', '610328', '140224', '530924', '520425', '532932', '610527', '511381', '620525', '140221', '522623', '513435', '420529', '140429', '141030', '431027', '131124', '520324', '340826', '431230', '130624', '140928', '422827', '532523', '131122', '620122', '450125', '411422', '532931', '520403', '130129', '410325', '130631', '520525', '520203', '130728', '430529', '340827', '610924', '533122', '141028', '522634', '411723', '140829', '451027', '130530', '361125', '610722', '141127', '360828', '422823', '640402', '532601', '130709', '522628', '610927', '141129', '540104', '411321', '520628', '513338', '140215', '140425', '510525', '540123', '130532', '130634']

    # year_list = [2020]
def filter_road_by_bound(district,year):
    df = pd.read_csv('../GT_csv/city_bounds_774_code_area.csv')

    district_list = [district]
    year_list = [year]
    if not os.path.exists('results_pixel_coored_final_shp_test/'):
        os.makedirs('results_pixel_coored_final_shp_test/')
    
    for district in district_list:
        for year in year_list:

            # district_chn = df[df['code']==int(district)]['county'].values[0]
            # # 1. 加载 Shapefile 和 GeoJSON

            if not os.path.exists('results_pixel_coored_final_shp_test/'+district+'_'+str(year)+'-GE-18-final-wgs.shp'):
                continue

            #if os.path.exists('results_pixel_coored_final_shp/'+district+'_'+str(year)+'-GE-18-final-wgs_inbound.shp'):
            #    continue
            print(district)
            
            edges = gpd.read_file('results_pixel_coored_final_shp_test/'+district+'_'+str(year)+'-GE-18-final-wgs.shp')  # 你的edge Shapefile路径
            boundary = gpd.read_file('../geojson/'+district+'.geojson')  # 你的GeoJSON路径

            # 假设 GeoJSON 只包含一个边界多边形
            boundary_polygon = boundary.unary_union  # 将多个几何图形合并为一个几何图形

            # 2. 过滤 Shapefile 中的边
            def clip_edge(line):
                # 使用shapely的intersection方法来裁剪边界外的线段
                if line.intersects(boundary_polygon):
                    return line.intersection(boundary_polygon)
                else:
                    return None

            # 将每个edge进行裁剪
            edges['geometry'] = edges['geometry'].apply(clip_edge)

            # 删除为空的几何形状
            edges = edges[~edges['geometry'].is_empty]

            # 3. 将过滤后的数据保存为新的 Shapefile
            edges.to_file('results_pixel_coored_final_shp_test/'+district+'_'+str(year)+'-GE-18-final-wgs_inbound.shp')
# filter_road_by_bound('130634',2020)
