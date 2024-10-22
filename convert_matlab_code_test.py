import cv2
import numpy as np
from skimage.morphology import square, skeletonize, remove_small_objects, label
from skimage.io import imread, imsave
from skimage.util import img_as_ubyte
import os
from PIL import Image
import matplotlib.pyplot as plt

Image.MAX_IMAGE_PIXELS = None  # 取消限制，或者设为更大的值

from skimage.measure import regionprops

def bwareaopen_python(image, min_size):
    # 标记连通区域
    labeled_img, num = label(image, connectivity=2, return_num=True)
    
    # 计算连通区域的面积
    for region in regionprops(labeled_img):
        if region.area < min_size:
            # 将小区域的像素设置为0
            labeled_img[labeled_img == region.label] = 0
    
    # 将图像转换为布尔类型
    return (labeled_img > 0).astype(np.uint8) * 255


def add_frame(image):
    # Add a white border around the image
    border_size = 10  # Example border size
    return cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=255)

# def IPNV_read(image_path):
#     return imread(image_path, as_gray=True)

def IPNV_read(image_path):
    # 读取图像为灰度图像
    image = imread(image_path, as_gray=True)
    
    # 将所有大于 0 的像素置为 255
    image[image > 0] = 1  # 先将大于 0 的部分设为 1（归一化）
    image = (image * 255).astype(np.uint8)  # 将 1 转为 255 并将图像转换为 8-bit 格式
    
    return image

def convert_matlab_code(district,year):
#'410926','622927', '411422', '130522','530626', '130925', '522635', '410225', '520602', '433124', '431128','130530'
# code_list = ['622901', '130532', '620102',  '131123', '620102', '130631', '130531', '131124', '610428', '411423', '630203', '130529', '341203', '361125', '622927', '411422', '130522', '522636', '131128', '520603',  '131122', '530626', '130925', '522635', '130434', '411327', '469024', '540524', '141034', '410225', '520602', '433124', '610328', '622924', '522630', '610430', '411424', '420921', '130533', '469029'] 
# ['610428', '411423', '630203', '130529', '341203', '361125',   '522636', '131128', '520603',  '131122',  '130434', '411327', '469024', '540524', '141034','610328', '622924', '522630', '610430', '411424', '420921', '130533', '469029']#131124
    code_list = [district]
    for code in code_list:
        print(code)
        input_picture_path = '../temp_output_test/'+district+'_GT_primary_'+str(year)+'.png'  #'../picture/'+code+'-17.png'  # replace with your input path
        output_picture_path = '../temp_output_test/'+district+'_GT_primary_'+str(year)+'-17-bone.png' #code+'-17-bone.png'  # replace with your output path

        if os.path.exists(output_picture_path):
            continue

        if not os.path.exists(input_picture_path):
            continue
        #     os.remove(output_picture_path)

        print('1.0->读入数据，确定测试单元')
        road_gray = IPNV_read(input_picture_path)

        print('2.0->膨胀腐蚀图像处理')
        if 1:#not os.path.exists(output_picture_path):
            # Convert grayscale image to 8-bit format
            road_gray = (road_gray * 255).astype(np.uint8)
            # road_gray[road_gray ==0 ] = 
            road_gray[road_gray ==1 ] = 255
            # road_gray[road_gray ==254 ] = 255
            # plt.imshow(road_gray)
            # plt.show()
            

            # Perform dilation, skeletonization, and other morphological operations
            road_imdilate = cv2.dilate(road_gray, square(5))
            np_array = np.array(road_imdilate)
            # print(np.where(np_array<255)[0])
            # plt.imshow(road_imdilate)
            # plt.show()
            road_skel = skeletonize(road_imdilate / 255).astype(np.uint8) * 255
            # plt.imshow(road_skel)
            # plt.show()
            road_spur = skeletonize(road_skel / 255).astype(np.uint8) * 255
            # plt.imshow(road_spur)
            # plt.show()

            # road_bone = remove_small_objects(road_spur.astype(bool), min_size=50).astype(np.uint8) * 255
            # 应用到 road_spur 图像
            road_bone = bwareaopen_python(road_spur, min_size=10)

            # Ensure the outermost pixels are set to 255
            road_bone[0, :] = 255
            road_bone[-1, :] = 255
            road_bone[:, 0] = 255
            road_bone[:, -1] = 255

            # plt.imshow(road_bone)
            # plt.show()

            # Save the result as an image
            imsave(output_picture_path, road_bone)
        # print(np.where(np.array(road_bone)==255))
    # else:
    #     road_bone = IPNV_read(output_picture_path)
# convert_matlab_code('130634',2020)