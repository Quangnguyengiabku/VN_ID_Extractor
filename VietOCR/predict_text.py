from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image
import cv2
import numpy as np
import time
def load_model():
    config = Cfg.load_config_from_name('vgg_transformer')
    # load pretrained weight
    config['weights'] = 'transformerocr.pth'

    # set device to use cpu
    config['device'] = 'cpu'
    config['cnn']['pretrained']=False
    config['predictor']['beamsearch']=False
    detector = Predictor(config)
    return detector
def text_recognition(image,detector):
    #config = Cfg.load_config_from_name('vgg_transformer')
    # load pretrained weight
    #config['weights'] = 'transformerocr.pth'

    # set device to use cpu
    #config['device'] = 'cpu'
    #config['cnn']['pretrained']=False
    #config['predictor']['beamsearch']=False

    #detector = Predictor(config)
    PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
    result = detector.predict(PIL_image)
    return result
if __name__=='__main__':
    image=cv2.imread('4.png')
    result=text_recognition(image)
    print(result)
