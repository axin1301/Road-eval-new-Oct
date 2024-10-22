import os
from PIL import Image
import pandas as pd
import math
import numpy as np
import geopandas as gpd
import PIL.Image
import cv2
PIL.Image.MAX_IMAGE_PIXELS = None
import matplotlib.pyplot as plt
import glob
import shutil
from PIL import Image
import argparse

def concat_all_label_image(year,district):

    if os.path.exists('../temp_output_test/'+district+'_GT_primary_'+str(year)+'.png'):
        return 0

    pred_img_list = glob.glob('../temp_output_test/'+district+'_road_label_by_image_'+str(year)+'/*.png')

    # df = pd.read_csv('../data/district_boundary_long_lat3.csv')
    # district_cn = list(df[df['latin']==district]['district'])[0]
    pd_dict = pd.read_csv('../data_test/tilefile_zl16_20_plus_20/'+ district+'.csv')

    y_tile_list = list(pd_dict['y_tile'])
    x_tile_list = list(pd_dict['x_tile'])

    # y_tile_list = [int(x.split('\\')[-1].split('.')[0].split('_')[0]) for x in pred_img_list]  ####Windows
    # y_tile_list = [int(x.split('/')[-1].split('.')[0].split('_')[0]) for x in pred_img_list]  ####Linux
    print(y_tile_list[:5]) ####[26072, 26073, 26074, 26074, 26075]

    # x_tile_list = [int(x.split('\\')[-1].split('.')[0].split('_')[1]) for x in pred_img_list] #Win
    # x_tile_list = [int(x.split('/')[-1].split('.')[0].split('_')[1]) for x in pred_img_list] ###Linux
    print(x_tile_list[:5]) ###[54001, 54002, 54002, 54003, 53999]

    min_x = min(x_tile_list)
    max_x = max(x_tile_list)
    min_y = min(y_tile_list)
    max_y = max(y_tile_list)
    print(min_x, max_x, min_y, max_y)

    mask_width_now = max_x-min_x+1
    mask_height_now = max_y-min_y+1

    # mask_now = max(mask_width_now, mask_height_now)
    mask_width = mask_width_now
    mask_height = mask_height_now
    print(mask_height_now, mask_width_now)

    mask_whole=np.zeros([mask_height*256,mask_width*256],dtype=int)

    for k in range(len(y_tile_list)):
        img_name = str(y_tile_list[k])+'_'+str(x_tile_list[k])
        if not os.path.exists('../temp_output_test/'+district+'_road_label_by_image_'+str(year)+'/' + img_name  +'.png'):
            continue
        
        img_temp=Image.open('../temp_output_test/'+district+'_road_label_by_image_'+str(year)+'/' + img_name  +'.png')
        mask_whole[(y_tile_list[k]-min_y)*256:(y_tile_list[k]-min_y+1)*256, (x_tile_list[k]-min_x)*256:(x_tile_list[k]-min_x+1)*256]=img_temp

    resized_img_tmp = Image.fromarray(mask_whole.astype(np.uint8))
    resized_img = resized_img_tmp.resize(((int(mask_width_now)*128,int(mask_height_now)*128)))  #####.resize((2048,2048)) ###resize 输出可以看看初步结果
    print(int(mask_width_now)*128,int(mask_height_now)*128)
    resized_img.save('../temp_output_test/'+district+'_GT_primary_'+str(year)+'.png')
