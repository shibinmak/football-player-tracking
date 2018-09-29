"""

** coded by shibinmak on 16/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
from keras.models import load_model
from preprocessing.simplepreprocessor import SimplePreprocessor
from preprocessing.imgtoarraypreprocessor import ImageToArrayPreprocessor
from utils.config import config
import cv2
import os
import numpy as np
import json
import tensorflow as tf
import keras.backend as K
import datetime




class Recognize:
    def __init__(self):
        self.means = json.loads(open(config.DATASET_MEAN).read())
        self.index = json.loads(open(config.PLAYER_INDEX).read())
        self.modelpath = os.path.join(config.MODEL_PATH, 'model.hdf5')
        self.model = load_model(self.modelpath)
        self.sp = SimplePreprocessor(100, 100)
        
        self.iap = ImageToArrayPreprocessor()

    def recognize(self, img, raw=False):
        #K.set_session(tf.keras.backend.get_session())
        if raw:
            image = cv2.imread(img)
        else:
            image = img

        prepro = [self.sp,self.iap]
        for i in prepro:
            image = i.preprocess(image)
        datacollection=image
        
        image = np.expand_dims(image, axis=0)


        pred = self.model.predict(image)
        max = pred.argmax(axis=1)
        score = (pred[0][max][0]) * 100
        label = self.index[str(max[0])]

        return label, score
