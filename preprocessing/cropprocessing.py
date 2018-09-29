"""

** coded by shibinmak on 14/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import cv2
import numpy as np


class cropPreprocesing:
    def __init__(self, width, height, horiz=True, inter=cv2.INTER_AREA):
        self.width = width
        self.height = height
        self.horiz = horiz
        self.inter = inter

    def preprocess(self, image):
        crops = []
        (h, w) = image.shape[:2]
        coords = [[0, 0, self.width, self.height],
                  [w - self.width, 0, w, self.height],
                  [w - self.width, h - self.height, w, h],
                  [0, h - self.height, self.height, w, h]]
        dw = int(0.5 * (w - self.width))
        dh = int(0.5 * (h - self.height))
        coords.append([dw, dh, w - dh, h - dh])

        for (startX, startY, endX, endY) in coords:
            crop = image[startY:endY, startX:endY]
            crop = cv2.resize(crop, (self.width, self.height), interpolation=self.inter)
            crops.append(crop)

        if self.horiz:
            mirrors = [cv2.flip(c) for c in crops]
            crops.extend(mirrors)

        return np.array(crops)
