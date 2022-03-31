
from Text_Detection.Text_Detection import TextDetector
from VietOCR.predict_text import text_recognition
from VietOCR.predict_text import load_model
import cv2
import csv
import codecs
import time


class TextExtractor: 
    def __init__(self):
        self.ID=None
        self.Name=None
        self.date=None
        self.hometown=None
        self.add=None
        self.DT=None
        self.TG=None
        self.provided_date=None
        self.NC=None
        self.detector_text=load_model() 

    ###############################################################################################

    def Text_Extraction(self,array_predict,img,type_image):
        array_predict=self.handle_array(array_predict)
        if type_image==1:
            print('Bạn đã chụp mặt trước của chứng minh nhân dân')
            ID=''
            Name=''
            Birth=''
            hometown=''
            add=''
            for i in range(array_predict.shape[0]):
                x=array_predict[i][1]
                y=array_predict[i][2]
                w=array_predict[i][3]
                h=array_predict[i][4]
                if array_predict[i][0]==4:
                    ID_img=img[y-7:y+h+7,x-7:x+w+7]
                    st_time=time.time()
                    ID=str(text_recognition(ID_img, self.detector_text))
                if array_predict[i][0]==7:
                    Name_img=img[y-7:y+h+7,x-7:x+w+7]
                    Line_name=text_recognition(Name_img, self.detector_text)
                    Name=str(Name)+' '+str(Line_name)
                if array_predict[i][0]==1:
                    Birth_img=img[y-7:y+h+7,x-7:x+w+7]
                    Birth=text_recognition(Birth_img, self.detector_text)
                if array_predict[i][0]==3:
                    Hometown_img=img[y-7:y+h+7,x-7:x+w+7]
                    line_Hometown=text_recognition(Hometown_img, self.detector_text)
                    hometown=str(hometown)+' '+str(line_Hometown)     
                if array_predict[i][0]==10:
                    add_img=img[y-7:y+h+7,x-7:x+w+7]
                    line_add=text_recognition(add_img, self.detector_text)
                    add=str(add)+' '+str(line_add)
            print('Số CMND           :',ID)
            print('Họ và tên         :',Name)
            print('Ngày sinh         :',Birth)
            print('Quê quán          :', hometown)
            print('Địa chỉ thường trú:',add)
            Data='"SOCMND":"'+str(ID)+'","HO_TEN":"'+str(Name)+'","NGAY_SINH":"'+str(Birth)+'","GIOI_TINH":"Nam",'+'"DIA_CHI":"'+str(add)+'"'
            #textpredict = "{} {} {} {} {}\n".format(ID, Name,Birth,hometown,add)
            #with codecs.open('save.txt','a+','utf-8') as f:
            #    f.write(textpredict)
            #return Data
        else: 
            print('Ban đã chụp mặt sau CMND')
            TG='Không'
            DT='Kinh'
            Day=''
            Month=''
            Year=''
            Noi_cap=''
            for i in range(array_predict.shape[0]):
                x=array_predict[i][1]
                y=array_predict[i][2]
                w=array_predict[i][3]
                h=array_predict[i][4]
                if array_predict[i][0]==0:
                    DT_img=img[y-7:y+h+7,x-7:x+w+7]
                    DT=text_recognition(DT_img, self.detector_text)
                if array_predict[i][0]==8:
                    TG_img=img[y-7:y+h+7,x-7:x+w+7]
                    TG=text_recognition(TG_img, self.detector_text)
                if array_predict[i][0]==2:
                    Day_img=img[y-7:y+h+7,x-7:x+w+7]
                    Day=text_recognition(Day_img, self.detector_text)
                if array_predict[i][0]==5:
                    Month_img=img[y-7:y+h+7,x-7:x+w+7]
                    Month=text_recognition(Month_img, self.detector_text) 
                if array_predict[i][0]==9:
                    Year_img=img[y-7:y+h+7,x-7:x+w+7]
                    Year=text_recognition(Year_img, self.detector_text)
                if array_predict[i][0]==6:
                    NC_img=img[y-7:y+h+7,x-7:x+w+7]
                    Noi_cap=text_recognition(NC_img, self.detector_text)
            NC=str(Day)+'.'+str(Month)+'.'+str(Year)
            print('Tôn giáo :',TG)
            print('Dân tộc  :',DT)
            print('Ngày cấp :',NC)
            print('Nơi cấp  :',Noi_cap)
            Data='"DAN_TOC":"'+str(DT)+'","QUOC_TICH":"Việt Nam"'+',"NGAY_CAP":"'+str(NC)+'","NOI_CAP":"'+str(Noi_cap)+'"'
            #textpredict = "{} {} {} {} \n".format(TG, DT,NC,Noi_cap)
            #with codecs.open('save.txt','a+','utf-8') as f:
            #    f.write(textpredict)
        return Data

    ###############################################################################################            
    def handle_array(self,array_predict):
        array_sort=sorted(array_predict[:,2])
        index_i=0
        index_j=0
        for i in array_sort:
            for j in array_predict:
                if j[2]==i:
                    array_predict[[index_i,index_j]]=array_predict[[index_j,index_i]]
                index_j+=1
            index_j=0
            index_i+=1
        return array_predict

if __name__=='__main__':
    quit    