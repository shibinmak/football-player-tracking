"""

** coded by shibinmak on 7/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
#aws
aws_acess_key = ""
aws_secret_key = ""
aws_region = ''

#folders
PROJECT_NAME = 'REALMADRID'
parentname = os.getcwd().split('/')[3]
parent = os.path.join(os.getenv('HOME'), parentname)
DATASET_FOLDER = os.path.join(parent, 'Dataset')

#detetction
ANNOT_PATH = os.path.sep.join([parent, 'data', 'annotations.csv'])

TRAIN_RECORD = os.path.sep.join([parent, 'data', 'records', 'training.record'])

TEST_RECORD = os.path.sep.join([parent, 'data', 'records', 'testing.record'])

CLASSES_FILE = os.path.sep.join([parent, 'data', 'records', 'classes.pbtxt'])

CLASSES = {'players': 1}
model_url = 'http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz'

TEST_SIZE = 0.25

#recognition



PLAYER_INDEX = os.path.join(parent, 'Dataset', 'playersindex.json')
MODEL_PATH = os.path.join(parent, "experiments", "exported_model")
DATASET_MEAN = os.path.join(parent, 'Dataset', "datasetmean.json")






