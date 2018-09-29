"""

** coded by shibinmak on 17/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""

import cv2
import imutils
import os
from HDF5fileutils.HDF5writer import HDF5Writer
import tensorflow as tf
from tensorflow import Session, Graph
import argparse
from utils.config import config
from recognize import Recognize
import numpy as np
from object_detection.utils import label_map_util
import keras.backend as K
import h5py
import datetime
import time

start = time.time()

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', help='input video', required=True)
args = vars(ap.parse_args())
modelpath = os.path.join(config.MODEL_PATH, 'frozen_inference_graph.pb')
hdf5data = os.path.join(os.getcwd(), 'tempdata.hdf5')
minc = 0.3
n = 1
#COLORS = np.random.uniform(0, 255, size=(n, 3))
COLORS = [[0,255,255]]

vinput = args['input']
split = vinput.split('/')
basename = split[-1]
filebase = basename[:basename.rfind('.') + 1].upper()
outputfile = config.PROJECT_NAME + '_' + filebase + 'avi'

stream = cv2.VideoCapture(vinput)
fps = stream.get(cv2.CAP_PROP_FPS)
width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
length = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

model = tf.Graph()

with model.as_default():
    graphDef = tf.GraphDef()

    with tf.gfile.GFile(modelpath, 'rb') as f:
        serializedGraph = f.read()
        graphDef.ParseFromString(serializedGraph)
        tf.import_graph_def(graphDef, name='')

labelMap = label_map_util.load_labelmap(config.CLASSES_FILE)
categories = label_map_util.convert_label_map_to_categories(labelMap, max_num_classes=1)
categoryIdx = label_map_util.create_category_index(categories)
FRAMES = 0
with model.as_default():
    with tf.Session(graph=model) as sess:
        hwriter = HDF5Writer(dims=(length, height, width, 3), outputpath=hdf5data)

        while True:
            (grabbed, frame) = stream.read()

            if not grabbed:
                break
            imageTensor = model.get_tensor_by_name('image_tensor:0')
            detectionBoxesTensor = model.get_tensor_by_name('detection_boxes:0')

            detectionScoresTensor = model.get_tensor_by_name('detection_scores:0')
            detectionClassesTensor = model.get_tensor_by_name('detection_classes:0')
            numDetection = model.get_tensor_by_name('num_detections:0')

            output = frame.copy()
            frame = imutils.resize(frame, width=int(width * 0.5), height=int(height * 0.5))

            (H, W) = frame.shape[:2]

            image = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
            image = np.expand_dims(image, axis=0)

            (boxes, scores, labels, N) = sess.run(
                [detectionBoxesTensor, detectionScoresTensor, detectionClassesTensor, numDetection],
                feed_dict={imageTensor: image})

            boxes = np.squeeze(boxes)
            scores = np.squeeze(scores)
            labels = np.squeeze(labels)
            data = list(zip(boxes, scores, labels))
            data.sort(key=lambda tup: tup[1], reverse=True)
            data = data[:20]
            boxes, scores, label = list(zip(*data))

            hwriter.add([output], [boxes], [scores], [label])

hwriter.close()

tf.keras.backend.clear_session()

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
writer = cv2.VideoWriter(outputfile, fourcc, 15, size, True)
tagged = []
graph1 = Graph()
with graph1.as_default():
    session1 = Session()
    with session1.as_default():
        rec = Recognize()
        data = h5py.File(hdf5data)
        for i in range(length):
            image = data['images'][i]
            boxes = data['boxes'][i]
            scores = data['scores'][i]
            labels = data['labels'][i]
            for box, score, label in zip(boxes, scores, labels):
                if score < minc:
                    continue

                (startY, startX, endY, endX) = box
                (H, W) = image.shape[:2]
                startY = int(startY * H)
                startX = int(startX * W)
                endY = int(endY * H)
                endX = int(endX * W)

                label = categoryIdx[label]
                idx = int(label["id"]) - 1
                #now = datetime.datetime.now().strftime("%M%S")
                #f = os.path.join(config.DATASET_FOLDER,'tf','{}{}.png'.format(i,str(now)))
                #cv2.imwrite(f,image[startY:endY, startX:endX])
                player, playerscore = rec.recognize(image[startY:endY, startX:endX])
                number = player.split('-')[0]
                name = player.split('-')[1]
                role = player.split('-')[2]
                
                playerdetails = '{}:{:.2f}%'.format(name, playerscore)
                
                
                cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 4)
                font = cv2.FONT_HERSHEY_SIMPLEX
                namesize = cv2.getTextSize(playerdetails, font, 0.75, 2)[0]
                rolesize = cv2.getTextSize(role, font, 0.50, 2)[0]
                X = int(startX+(endX-startX) / 2)
                
                Y = startY - rolesize[1] if startY - rolesize[1] > 10 else startY
                Y = int(Y)

                cv2.putText(image, role, (X, Y), font, 0.50, COLORS[idx], 2)
                cv2.putText(image, playerdetails, (X, Y-namesize[1]), font, 0.75, COLORS[idx], 2)
                
            writer.write(image)
        data.close()
        writer.release()
        stream.release()
        os.remove(hdf5data)
K.clear_session()
stop = time.time() - start
print('\n \n \n[INFO] TIME TAKEN:{:.2f} seconds'.format(stop))
