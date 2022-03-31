import cv2
import matplotlib.pyplot as plt
import numpy as np
import glob
import time
import os 
import random
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class IDDetector: 

    def __init__(self): 
        self.yolo_weights = os.path.exists(os.path.join(CURRENT_DIR, "yolov4-custom_last.weights"))
        if ( self.yolo_weights== False):
            print("ERROR:lack file yolov4-custom_last.weights")
            quit()
        self.yolo_cfg = os.path.exists(os.path.join(CURRENT_DIR, "yolov4-custom.cfg"))
        if ( self.yolo_cfg== False):
            print("ERROR:lack file yolov4-custom.cfg")
            quit()
        self.yolo_name = os.path.exists(os.path.join(CURRENT_DIR, "yolo.names"))
        if ( self.yolo_name== False):
            print("ERROR:lack file yolo.names")
            quit()
        with open(os.path.join(CURRENT_DIR, "yolo.names"), 'r') as f: # Edit CLASS file
            classes = [line.strip() for line in f.readlines()]
        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
        self.net = cv2.dnn.readNet(os.path.join(CURRENT_DIR, "yolov4-custom_last.weights"),os.path.join(CURRENT_DIR, "yolov4-custom.cfg")) # Edit WEIGHT and CONFIC file
        layer_names=self.net.getLayerNames()
        self.output_layers=[layer_names[i[0]-1] for i in self.net.getUnconnectedOutLayers()] 
    ####################################################################################################################################################
    
    def detectID(self,image):
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392
        classes = None
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes=[]
        conf_threshold=0.3
        nms_threshold=0.4
        for out in outs:
            for detection in out: 
                scores=detection[5:]
                class_id=np.argmax(scores)
                confidence=scores[class_id]
                if confidence >0.05: 
                    center_x=int(detection[0]*Width)
                    center_y=int(detection[1]*Height)
                    w=int(detection[2]*Width)
                    h=int(detection[3]*Height)
                    x=center_x-w/2
                    y=center_y-h/2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x,y,w,h])
        indices=cv2.dnn.NMSBoxes(boxes,confidences,conf_threshold,nms_threshold)
        if len(indices)==0: 
            t= np.array((0,0,0,0),dtype=int)
            return t
        Result=""
        count=indices.shape[0]
        array_predict=np.zeros((count,5),dtype=int)
        count=0
        for i in indices:
            i=i[0]
            box=boxes[i]
            x=round(box[0])
            y=round(box[1])
            w=round(box[2])
            h=round(box[3])
            array_predict[count][0]=class_ids[i]
            array_predict[count][1]=x
            array_predict[count][2]=y
            array_predict[count][3]=w
            array_predict[count][4]=h
            count=count+1
            textpredict="{} {} {}\n".format(str(class_ids[i]),x+w/2,y+h/2)
            #self.draw_prediction(image, class_ids[i],confidences[i], round(x), round(y), round(x + w), round(y + h),classes,COLORS)
            Result +=textpredict
        file=open("test.txt","w+")
        file.write(Result)
        file.close()
        return array_predict
    ####################################################################################################################################################
    
    def draw_prediction(self,img,class_id,confidence,x,y,x_plus_w,y_plus_h,classes,COLORS):
        self.label=str(classes[class_id])
        self.color=COLORS[class_id]
        cv2.rectangle(img,(x,y),(x_plus_w,y_plus_h),self.color,2)
        cv2.putText(img,self.label+' '+ str(confidence),(x-10,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.75,self.color,2)
    ####################################################################################################################################################

    def draw(self,image,points):
        height,width=image.shape[:2]
        for (self.label,xi,yi,wi,hi) in points: 
            center_x=int(xi*width)
            center_y=int(yi*height)
            w=int(wi*width)
            h=int(hi*height)
            #Rectangle coordinates:
            x=int(center_x-w/2)
            y=int(center_y-h/2)
            cv2.rectangle(image,(x,y),(x+w,y+h))
        return 
    ####################################################################################################################################################
        
    def savePredict(self,name,text):
        textName=name+'.txt'
        with open(textName,'w+') as groundTruth: 
            groundTruth.write(text)
            groundTruth.close()

    def DetectIDFromImg(self,filepath):
        image=cv2.imread(filepath)
        return self.detectID(image)
####################################################################################################################################################

ID_Detect=IDDetector()
if __name__=='__main__':
    #image="WIN_20211005_11_11_03_Pro.jpg"
    image="WIN_20211020_10_35_06_Pro_jpg.rf.54bb182cf567dd094f91e2565a000e10.jpg"
    image,label,conf=ID_Detect.DetectIDFromImg(image)
    cv2.imshow("object detection", image)
    cv2.waitKey(5000)
    print(label,conf)
    cv2.destroyAllWindows()