"""

** coded by shibinmak on 14/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import h5py
import os
import numpy as np


class HDF5Writer:
    def __init__(self, dims, outputpath, buffsize=5):

        #if os.path.exists(outputpath):
            #raise ValueError("FILE ALREADY EXISTS,CANT BE OVERWRITTEN")

        self.db = h5py.File(outputpath, 'w')
        
        self.images = self.db.create_dataset('images', dims, dtype=np.uint8)
        self.boxes = self.db.create_dataset('boxes', (dims[0],20,4),dtype='float')
        self.scores = self.db.create_dataset('scores', (dims[0],20),dtype='float')
        self.labels = self.db.create_dataset('labels', (dims[0],20),dtype='float')

        self.buffsize = buffsize
        self.buffer = {'images': [], 'boxes': [],'scores':[],'labels':[]}
        self.idx = 0

    def add(self, image, boxes,scores,labels):
        self.buffer['images'].extend(image)
        self.buffer['boxes'].extend(boxes)
        self.buffer['scores'].extend(scores)
        self.buffer['labels'].extend(labels)

        if len(self.buffer['images']) >= self.buffsize:
            self.flush()

    def flush(self):
        i = self.idx + len(self.buffer['images'])
        self.images[self.idx:i] = self.buffer['images']
        self.boxes[self.idx:i] = self.buffer['boxes']
        self.scores[self.idx:i] = self.buffer['scores']
        self.labels[self.idx:i] = self.buffer['labels']
        self.idx = i
        self.buffer = {'images': [], 'boxes': [],'scores':[],'labels':[]}


    def close(self):
        if len(self.buffer['images']) > 0:
            self.flush()
        self.db.close()
