
import os 
import cv2
import numpy as np
import imutils
import math 
from Card_alignment.card_alignment import CardAlignment
os.path.dirname(os.path.abspath(__file__))
Align=CardAlignment()
from Pretreatment.Yolo_Detection.ID_Detector import  IDDetector

class Alignment: 
    def __init__(self): 
        self.alpha=0.2
    def xoay_nguoc_chieu(self,crop_image,w,h):
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
            else: angles=abs((angles_image_ori-32.23)*2.75)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=1)
        # Rotate the image using cv2.warpAffine
        rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
        # Rotate the image using cv2.warpAffine
        #cv2.waitKey(0)
        # write the output, the rotated image to disk
        cv2.imwrite('rotated_image.jpg', rotated_image)
        self.rotated_image=rotated_image
        return self.rotated_image
    def xoay_cung_chieu(self,crop_image,w,h):
        height, width = crop_image.shape[:2]
        center = (width/2, height/2)
        # the above center is the center of rotation axis
        # use cv2.getRotationMatrix2D() to get the rotation matrix
        angles_image_ori=math.atan(h/w)*180/math.pi
        if(angles_image_ori>45):
            angles=-abs((angles_image_ori-32.23)*3.5)
        else:
            if angles_image_ori<35:
                angles=-abs((angles_image_ori-32.23)*2)
            else: angles=-abs((angles_image_ori-32.23)*2.75)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=0.8)
        # Rotate the image using cv2.warpAffine
        rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
        self.rotated_image=rotated_image
        return self.rotated_image
    def xoay_180_do(self,crop_image):
        height, width = crop_image.shape[:2]
        center = (width/2, height/2)
        # the above center is the center of rotation axis
        # use cv2.getRotationMatrix2D() to get the rotation matrix
        angles=180
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angles, scale=0.8)
        # Rotate the image using cv2.warpAffine
        rotated_image = cv2.warpAffine(src=crop_image, M=rotate_matrix, dsize=(width, height))
        self.rotated_image=rotated_image
        return self.rotated_image
    def xu_li_mat_truoc(self,ori_image,array_detect,i,j):
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
        crop_image=ori_image[max(0,y-100):min(y+h+100,ori_image.shape[0]),max(0,x-100):min(x+w+100,ori_image.shape[1])]
        if center_quoc_huy_x<x+w/2: 
            if 0<center_quoc_huy_y<y+h/2-int(self.alpha*w):
                rotation_image=self.xoay_nguoc_chieu(crop_image,w,h)
            else: 
                rotation_image=self.xoay_cung_chieu(crop_image,w,h)
            processed_image=Align.scan_card(rotation_image,None)   
        else: 
            crop_image=self.xoay_180_do(crop_image)
            if 0<center_quoc_huy_y<y+h/2:
                rotation_image=self.xoay_cung_chieu(crop_image,w,h)
            else:
                rotation_image=self.xoay_nguoc_chieu(crop_image,w,h)
            processed_image=Align.scan_card(rotation_image,None)
        self.processed_image=processed_image
        return self.processed_image

    def xu_li_mat_sau(self,ori_image,array_detect,i,j):
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
        crop_image=ori_image[max(0,y-100):min(y+h+100,ori_image.shape[0]),max(0,x-100):min(x+w+100,ori_image.shape[1])]
        if center_quoc_huy_x<x+w/2: 
            if 0<center_quoc_huy_y<y+h/2-int(self.alpha*w):
                rotation_image=self.xoay_nguoc_chieu(crop_image,w,h)
            else: 
                rotation_image=self.xoay_cung_chieu(crop_image,w,h)
            processed_image=Align.scan_card(rotation_image,None)   
        else: 
            crop_image=self.xoay_180_do(crop_image)
            if 0<center_quoc_huy_y<y+h/2:
                rotation_image=self.xoay_cung_chieu(crop_image,w,h)
            else:
                rotation_image=self.xoay_nguoc_chieu(crop_image,w,h)
            processed_image=Align.scan_card(rotation_image,None)
        #cv2.imshow('crop_image',ori_image)
        #cv2.waitKey(0)
        self.processed_image=processed_image
        return self.processed_image

    def AlignmentImage(self,image):
        #image = imutils.resize(image, height = int(self.RESCALED_HEIGHT))
        ori_image=image
        array_detect=ID_Detect.detectID(image)
        if array_detect.shape[0]==2:
            if array_detect[0][0]==2: 
                i=0
                j=1
                processed_image=self.xu_li_mat_truoc(ori_image,array_detect,i,j)
                type_image=1
            elif array_detect[1][0]==2:
                i=1
                j=0
                processed_image=self.xu_li_mat_truoc(ori_image,array_detect,i,j)
                type_image=1
            elif array_detect[0][0]==1:
                i=0
                j=1
                processed_image=self.xu_li_mat_sau(ori_image,array_detect,i,j)
                type_image=2
            elif array_detect[1][0]==1:
                i=1
                j=0
                processed_image=self.xu_li_mat_sau(ori_image,array_detect,i,j)
                type_image=2
            else: 
                processed_image=np.array([0],dtype=int)
                type_image=0
        else:
            processed_image=np.array([0],dtype=int)
            type_image=0
        self.processed_image=processed_image
        self.type_image=type_image
        return self.processed_image,self.type_image

##########################################################################################################
ID_Detect=IDDetector()
Alignment_ID=Alignment()
if __name__=='__main__':
    image=cv2.imread('214292537_510173723372734_3636461390872080889_n_jpg.rf.acdcc2f898986fc499c5329796f56527.jpg')
    processed_image=Alignment_ID.AlignmentImage(image)
    cv2.imshow("object detection",processed_image)
    cv2.waitKey(5000)