"""

** coded by shibinmak on 8/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
import time
#os.system('conda install tensorflow-gpu')

os.system('sudo apt-get install protobuf-compiler python-pil python-lxml python-tk')
os.system('pip install tensorflow-gpu')
os.system('pip install --user Cython')

os.system('pip install --user contextlib2')
os.system('pip install opencv-python')
os.system('pip install --user jupyter')
os.system('pip install --user matplotlib')
os.system('pip install --user Pillow')
os.system('pip install --user imutils')
os.system('pip install --user lxml')

os.chdir(os.getenv('HOME'))
os.system('git clone https://github.com/tensorflow/models.git')
rfolder = os.path.join(os.getcwd(), 'models/research')

os.chdir(os.getenv('HOME'))
os.system('git clone https://github.com/cocodataset/cocoapi.git')
os.chdir(os.path.join(os.getcwd(), 'cocoapi/PythonAPI'))
os.system('make')
os.system('cp -r pycocotools {}'.format(rfolder))

os.chdir(rfolder)
os.system('protoc object_detection/protos/*.proto --python_out=.')
pp = "#!/bin/sh \n \nexport PYTHONPATH='$PYTHONPATH:{}:{}/slim'".format(rfolder, rfolder)

ppsh = os.path.join(os.getcwd(), 'ppsetup.sh')

shfile = open(ppsh, 'w')
shfile.write(pp)
shfile.close()

time.sleep(2)

os.system('bash ppsetup.sh')

os.chdir(rfolder)

os.system('python3 object_detection/builders/model_builder_test.py')



