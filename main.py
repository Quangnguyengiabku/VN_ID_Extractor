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
from post_data import post_data
import json

#Goi class
Card_Alignment = Alignment()
Text_Detector = TextDetector()
Text_Extractor=TextExtractor()


#url = 'http://192.168.100.9:8080/video'
count=0
img_counter = 0
cam = cv2.VideoCapture(0)
while True:
    #start camera:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    k = cv2.waitKey(1)
    image=frame.copy()
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    #Chup va xu li mat truoc: 

    if count==0:
        cv2.putText(frame,'Nhan F de chup mat truoc CMND',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        try:
            if k%256 ==102:
                try:
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    #cv2.imwrite(img_name, frame)
                    cv2.imshow("photo", image)
                    st_time=time.time()
                    Algined_image,type_image=Card_Alignment.AlignmentImage(image)
                    if type_image==0 or type_image==2:
                        print('Anh chup khong hop le:')
                        a=1/0
                        continue
                    array_text_predict,img=Text_Detector.detectText(Algined_image)
                    if array_text_predict.shape[0]==3:
                        print('Vui long chup lai hinh moi:')
                        a=1/0
                        continue
                    Data_F=Text_Extractor.Text_Extraction(array_text_predict,img,type_image)
                    end_time=time.time()
                    print(end_time-st_time,'s')
                    print("{} written!".format(img_name))
                    print('Nhấn nút bất kì để tiếp tục:')
                    count+=1
                    #cv2.putText(frame,'Please Press F  to take a photo',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
                    print('---------------------------------------------------')        
                except:
                    print('Nhấn nút bất kì để tiếp tục:')
                    t=cv2.waitKey(0)  
            else:
                1/0      
        except:
            pass
    #Chup va xu li mat sau:
    if count==1:
        cv2.putText(frame,'Nhan B de chup mat sau CMND',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        try:
            if k%256 ==98:
                try:
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    #cv2.imwrite(img_name, frame)
                    cv2.imshow("photo", image)
                    st_time=time.time()
                    Algined_image,type_image=Card_Alignment.AlignmentImage(image)
                    if type_image==0 or type_image==1:
                        print('Anh chup khong hop le:')
                        1/0
                    array_text_predict,img=Text_Detector.detectText(Algined_image)
                    if array_text_predict.shape[0]==3:
                        print('Vui long chup lai hinh moi:')
                        1/0
                    Data_B=Text_Extractor.Text_Extraction(array_text_predict,img,type_image)
                    end_time=time.time()
                    print(end_time-st_time,'s')
                    print('Nhấn nút bất kì để tiếp tục:')
                    count+=1
                    print('---------------------------------------------------')        
                except:
                    print('Nhấn nút bất kì để tiếp tục:')
                    t=cv2.waitKey(0)  
            else:
                1/0      
        except:
            pass
        if count==2:
            count=0
            print('Ban da chup xong 2 mat')
            #Data='{'+str(Data_F)+','+str(Data_B)+'}'
            #Data=json.loads(Data)
            #post_data(Data)
    cv2.imshow("Camera", frame)
cam.release()
cv2.destroyAllWindows()


        


