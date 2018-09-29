"""

** coded by shibinmak on 14/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
from keras.preprocessing.image import img_to_array


class ImageToArrayPreprocessor:
    def __init__(self, dataFormat=None):
        self.dataFormat = dataFormat

    def preprocess(self, image):
        return img_to_array(image, data_format=self.dataFormat)
