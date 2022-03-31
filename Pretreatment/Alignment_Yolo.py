from Yolo_Detection.ID_Detector import  IDDetector
import os 
import cv2
import numpy as np
import imutils
import math 
alpha=0.2
def xoay_nguoc_chieu(crop_image,w,h):
    height, width = crop_image.shape[:2]
    center = (width/2, height/2)
    # the above center is the center of rotation axis
    # use cv2.getRotationMatrix2D() to get the rotation matrix
    angles_image_ori=math.atan(h/w)*180/math.pi
    if(angles_image_ori>45):
        angles=abs((angles_image_ori-32.23)*3.5)
    else:
        if angles_image_ori<35:
            angles=abs((angles_image_ori-32.23)*2)
        else: angles=abs((angles_image_ori-32.23)*3)
    print(angles)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=1)
    # Rotate the image using cv2.warpAffine
    rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
    # Rotate the image using cv2.warpAffine
    #cv2.waitKey(0)
    # write the output, the rotated image to disk
    cv2.imwrite('rotated_image.jpg', rotated_image)
    return rotated_image
def xoay_cung_chieu(crop_image,w,h):
    height, width = crop_image.shape[:2]
    center = (width/2, height/2)
    # the above center is the center of rotation axis
    # use cv2.getRotationMatrix2D() to get the rotation matrix
    angles_image_ori=math.atan(h/w)*180/math.pi
    print(angles_image_ori)
    if(angles_image_ori>45):
        angles=-abs((angles_image_ori-32.23)*3.5)
    else:
        if angles_image_ori<35:
            angles=-abs((angles_image_ori-32.23)*2)
        else: angles=-abs((angles_image_ori-32.23)*3)
    print(angles)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=0.9)
    # Rotate the image using cv2.warpAffine
    rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
    # Rotate the image using cv2.warpAffine
    # visualize the original and the rotated image
    # wait indefinitely, press any key on keyboard to exit
    #cv2.waitKey(0)
    # write the output, the rotated image to disk
    #cv2.imwrite('rotated_image.jpg', rotated_image)
    return rotated_image
def xoay_180_do(crop_image):
    height, width = crop_image.shape[:2]
    center = (width/2, height/2)
    # the above center is the center of rotation axis
    # use cv2.getRotationMatrix2D() to get the rotation matrix
    angles=180
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=0.9)
    # Rotate the image using cv2.warpAffine
    rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
    return rotated_image
def xu_li_mat_truoc(ori_image,array_detect,i,j):
    x=max(0,array_detect[i][1])
    y=max(0,array_detect[i][2])
    w=array_detect[i][3]
    h=array_detect[i][4]
    x_quoc_huy=array_detect[j][1]
    y_quoc_huy=array_detect[j][2]
    w_quoc_huy=array_detect[j][3]
    h_quoc_huy=array_detect[j][4]
    center_quoc_huy_x=x_quoc_huy+w_quoc_huy/2
    center_quoc_huy_y=y_quoc_huy+h_quoc_huy/2
    crop_image=ori_image[y:(y+h),x:(x+w)]
    if center_quoc_huy_x<x+w/2: 
        if 0<center_quoc_huy_y<y+h/2-int(alpha*w):
            rotation_image=xoay_nguoc_chieu(crop_image,w,h)
        else: 
            rotation_image=xoay_cung_chieu(crop_image,w,h)
    else: 
        crop_image=xoay_180_do(crop_image)
        if 0<center_quoc_huy_y<y+h/2:
            rotation_image=xoay_cung_chieu(crop_image,w,h)
        else:
            rotation_image=xoay_nguoc_chieu(crop_image,w,h)
    #crop_image=ori_image[y:(y+h),x:(x+w)]
    #cv2.imshow('crop_image',ori_image)
    #cv2.waitKey(0)
    path_save=os.path.join('output',file)
    cv2.imwrite(path_save,rotation_image)
def xu_li_mat_sau(ori_image,array_detect,i,j):
    x=max(0,array_detect[i][1])
    y=max(0,array_detect[i][2])
    w=array_detect[i][3]
    h=array_detect[i][4]
    x_quoc_huy=array_detect[j][1]
    y_quoc_huy=array_detect[j][2]
    w_quoc_huy=array_detect[j][3]
    h_quoc_huy=array_detect[j][4]
    center_quoc_huy_x=x_quoc_huy+w_quoc_huy/2
    center_quoc_huy_y=y_quoc_huy+h_quoc_huy/2
    crop_image=ori_image[y:(y+h),x:(x+w)]
    if center_quoc_huy_x<x+w/2: 
        if 0<center_quoc_huy_y<y+h/2-int(alpha*w):
            ori_image=xoay_nguoc_chieu(crop_image,w,h)
        else: 
            ori_image=xoay_cung_chieu(crop_image,w,h)
    else: 
        crop_image=xoay_180_do(crop_image)
        if 0<center_quoc_huy_y<y+h/2:
            ori_image=xoay_cung_chieu(crop_image,w,h)
        else:
            ori_image=xoay_nguoc_chieu(crop_image,w,h)
    path_save=os.path.join('output',file)
    cv2.imwrite(path_save,ori_image)

ID_Detect=IDDetector()
listfile=os.listdir('Input')
for file in listfile:
    path=os.path.join('Input',file)
    image=cv2.imread(path)
    '''
    if image.shape[1]>2000:
        RESCALED_HEIGHT=1600
        image = imutils.resize(image, height = int(RESCALED_HEIGHT))
    if image.shape[1]>1000:
        RESCALED_HEIGHT=800
        image = imutils.resize(image, height = int(RESCALED_HEIGHT))
    '''
    ori_image=image
    array_detect=ID_Detect.detectID(image)
    #cv2.imshow('image',image)
    #cv2.waitKey(0)
    if array_detect.shape[0]==2:
        if array_detect[0][0]==2: 
            i=0
            j=1
            xu_li_mat_truoc(ori_image,array_detect,i,j)
        elif array_detect[1][0]==2:
            i=1
            j=0
            xu_li_mat_truoc(ori_image,array_detect,i,j)
        elif array_detect[0][0]==1:
            i=0
            j=1
            xu_li_mat_sau(ori_image,array_detect,i,j)
        elif array_detect[1][0]==1:
            i=1
            j=0
            xu_li_mat_sau(ori_image,array_detect,i,j)
        else: 
            print('Vui long chup lai cmnd')
    else:
        print('Vui long Chup lai cmnd:',path)