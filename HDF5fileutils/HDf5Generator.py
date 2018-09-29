"""

** coded by shibinmak on 14/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
from keras.utils import np_utils
import numpy as np
import h5py


class HDF5Generator:
    def __init__(self, dbpath, batchSize, classes, preprocessors=None, aug=None, binarize=True):

        self.batchSize = batchSize
        self.aug = aug
        self.dbpath = dbpath
        self.binarize = binarize
        self.clasees = classes
        self.db = h5py.File(dbpath)
        self.numImages = self.db['labels'].shape[0]
        self.preprocessors = preprocessors

    def generator(self, passes=np.inf):

        epochs = 0
        while epochs < passes:
            for i in range(0, self.numImages, self.batchSize):
                images = self.db['images'][i:i + self.batchSize]
                labels = self.db['labels'][i:i + self.batchSize]

                if self.binarize:
                    labels = np_utils.to_categorical(labels, self.clasees)
                if self.preprocessors is not None:
                    procImages = []
                    for image in images:
                        for p in self.preprocessors:
                            image = p.preprocess(image)

                        procImages.append(image)

                    images = np.array(procImages)
                if self.aug is not None:
                    (images, labels) = next(self.aug.flow(images, labels, batch_size=self.batchSize))

                yield (images, labels)

            epochs += 1

    def close(self):
        self.db.close()
