import cv2 
import imutils
import numpy as np
from Pretreatment.Alignment_Image import Alignment
from Card_alignment.card_alignment import CardAlignment
from Text_Detection.Text_Detection import Text_Detection, TextDetector
from Text_Recognition.Text_Recognition import TextExtractor
import os
import csv
import time

Card_Alignment = Alignment()
Text_Detector = TextDetector()
Text_Extractor=TextExtractor()

#url = 'http://192.168.100.9:8080/video'
count=0
img_counter = 0
dir=os.path.join('Image_test')
listfile=os.listdir(dir)
for file in listfile:
    count+=1
    print(str(count)+':'+file) 
    path=os.path.join(dir,file)
    image=cv2.imread(path)
    #PHÁT HIỆN VÀ HIỆU CHỈNH ẢNH CMND CHO THẲNG GÓC.
    Algined_image,type_image=Card_Alignment.AlignmentImage(image)
    if type_image==0:
        print('Anh chup khong hop le:')
        continue
    #PHÁT HIỆN VÙNG ẢNH CHỨA ĐẶC TRƯNG CẦN TRÍCH XUẤT
    array_text_predict,img=Text_Detector.detectText(Algined_image)
    if array_text_predict.shape[0]==3:
        print('Vui long chup lai hinh moi:')
        continue
    st_time=time.time()
    #TRÍCH XUẤT CHỮ
    Text_Extractor.Text_Extraction(array_text_predict,img,type_image)
    end_time=time.time()
    print(end_time-st_time,'s')
    print('---------------------------------------------------')
cam.release()
''' 
cv2.destroyAllWindows()
for file in listfile:
    count+=1
    print(str(count)+':'+file) 
    path=os.path.join(dir,file)
    image=cv2.imread(path)
    Algined_image,type_image=Card_Alignment.AlignmentImage(image)
    if type_image==0:
        print('Anh chup khong hop le:')
        continue
    array_text_predict,img=Text_Detector.detectText(Algined_image)
    if array_text_predict.shape[0]==3:
        print('Vui long chup lai hinh moi:')
        continue
    st_time=time.time()
    Text_Extractor.Text_Extraction(array_text_predict,img,type_image)
    end_time=time.time()
    print(end_time-st_time,'s')
    print('---------------------------------------------------')
#print(array_text_predict)
#print(img.shape)
#cv2.imshow('t',img)
#cv2.waitKey(0)
'''

        


