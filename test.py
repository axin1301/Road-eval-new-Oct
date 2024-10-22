# l = ['510524', '130724', '520602', '610525', '430524', '630223', '511722', '621221', '500114', '610630', '520603', '530129', '610830', '610327', '522727', '451024', '513434', '421126', '540426', '610528', '431226', '532329', '540237', '422822', '622926', '341221', '532625', '411425', '653101', '540121', '360881', '530602', '610724', '421122', '230826', '621121', '431382', '230129', '532528', '451224', '532923', '530902', '150927', '530823', '420381', '622925', '451081', '532926', '231222', '620822', '540525', '621228', '421121', '522626', '530626', '451226', '610429', '410526', '623024', '469025', '411326', '411725', '530927', '130627', '520423', '422825', '140924', '140926', '630202', '341522', '410926', '230231', '532529', '530502', '150429', '530921', '411627', '360703', '621122', '630222', '431322', '540523', '411522', '532327', '540524', '532823', '653123', '140932', '654022', '530523', '532530', '522629', '610925', '610829', '610828', '361030', '532927', '530925', '522323', '653201', '230422', '532624', '140922', '341722', '520622', '513327', '522728', '622921', '469029', '622924', '532924', '451029', '360424', '513226', '340422', '140623', '410324', '621026', '640425', '640422', '430923', '140930', '653121', '511133', '360731', '421123', '530621', '433122', '141123', '522723', '630123', '150926', '621021', '530722', '621027', '513323', '513221', '610621', '611025', '500230', '431221', '422801', '431022', '513429', '140925', '632322', '360734', '431227', '141032', '411722', '361025', '610726', '533123', '130726', '130722', '630224', '431223', '513225', '532626', '530128', '611022', '410423', '622922', '431026', '540103', '433126', '341225', '540124', '451424', '522726', '610725', '653124', '520325', '610428', '141031', '360827', '431229', '511129', '411330', '450124', '130723', '421181', '621225', '420922', '341321', '451324', '150125', '530622', '411729', '500229', '511902', '520381', '141128', '360732', '611023', '411424', '653122']

# l = ['532530', '341225', '532823', '630123', '610528', '433122', '341221', '610828', '610725', '360424', '620822', '360827', '530622', '522629', '610726', '610630', '540237', '140924', '621021', '530602', '410423', '422825', '411722', '230231', '431022', '431223', '513225', '451224', '532329', '513327', '510524', '140926', '469025', '532927', '530902', '520325', '431226', '422822', '540121', '610724', '520423', '231222', '532625', '451024', '150926', '451226', '140623', '411326', '421123', '530823', '530523', '411425', '431227', '621122', '451029', '522723', '621221', '150429', '360731', '610925', '130627', '532923', '611023', '411522', '130726', '530129', '500229', '421181', '341522', '630202', '230129', '611022', '141128', '420922', '522727', '430524', '411330', '361025', '411627', '540525', '653122', '530722', '430923', '532624', '532626', '431026', '522726', '140925', '451424', '141031', '533123', '451081', '140930', '422801', '532926', '630223', '522728', '532528', '530921', '610830', '540523', '530925', '360732', '640425', '630224', '431382', '610621', '610429', '611025', '511133', '630222', '511722', '653121', '360703', '150927', '451324', '130723', '360734', '431322', '530502', '513221', '632322', '610327', '450124', '530128', '532327', '411725', '140922', '540103', '532529', '513323', '532924', '530927', '420381', '431229', '140932', '623024', '421126', '621026', '340422', '410324', '141123']
# print(len(l))

# import geopandas as gpd
# import matplotlib.pyplot as plt

# gdf = gpd.read_file('../geojson/130530.geojson')
# gdf.plot()
# plt.show()

#38.63215554955093, 114.69288051501672
#38.61357502589539, 114.69160463418187

#38.62354371653719, 114.69874956685705
#38.62083236985777, 114.71962297731521

#38.6146118342741, 114.70114822282655
#38.60216914475737, 114.71610154621102



# import numpy as np

# def generate_lat_lon_curve(start, end, num_points=10):
#     # 分别对经度和纬度进行线性插值
#     lats = np.linspace(start[0], end[0], num_points)
#     lons = np.linspace(start[1], end[1], num_points)
#     # 将经纬度组合成字符串列表
#     curve = [f"{lon},{lat}" for lat, lon in zip(lats, lons)]
#     return ";".join(curve)

# # 三组起点和终点的经纬度
# coordinates = [
#     ((38.63215554955093, 114.69288051501672), (38.61357502589539, 114.69160463418187)),
#     ((38.62354371653719, 114.69874956685705), (38.62083236985777, 114.71962297731521)),
#     ((38.6146118342741, 114.70114822282655), (38.60216914475737, 114.71610154621102)),
#     ((39.36272587911145, 115.4837390850658),(39.343080651614905, 115.53214759401455))
# ]

# # 生成每组经纬度曲线的结果
# results = [generate_lat_lon_curve(start, end) for start, end in coordinates]

# # 输出结果
# for i, result in enumerate(results, 1):
#     print(f"第{i}组曲线：{result}")

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

fig, ax = plt.subplots(figsize=(10, 10))

gdf = gpd.read_file('results_pixel_coored_final_shp/130634_2020-GE-18-final-wgs_inbound.shp')
gdf.plot(ax=ax, color='orange', edgecolor='black')

# 1. 读取CSV文件
csv_file = '../GT_csv/GT_GaoDe.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(csv_file)

# 2. 解析经纬度列表
    # 假设经纬度列表在第3列（索引为2）
    # 3. 绘制曲线

for k in [11,12,13]:
    latlong_str = df.iloc[k, 2]

    # 将字符串拆分成经纬度对，并解析成浮点数列表
    coordinates = [
        tuple(map(float, point.split(','))) 
        for point in latlong_str.split(';')
    ]

    # 分离经度和纬度
    longitudes, latitudes = zip(*coordinates)

    # 4. 绘制经纬度路径
    ax.plot(longitudes, latitudes, marker='o', linestyle='-', color='b', linewidth=2, label='Path')

    # 添加标题和图例
ax.set_title('Shapefile with Latitude and Longitude Path')
ax.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid()
plt.show()