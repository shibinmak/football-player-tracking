"""

** coded by shibinmak on 14/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""

import cv2
import os


class MeanPreprocessor:

    def __init__(self, rMean, gMean, bMean):
        self.rMean = rMean
        self.gMean = gMean
        self.bMean = bMean

    def preprocess(self, image):
        (B, G, R) = cv2.split(image.astype("float32"))

        R -= self.rMean
        G -= self.gMean
        B -= self.bMean

        return cv2.merge([B, G, R])
