"""

** coded by shibinmak on 8/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
from config import config

parent = config.parent
model_url = config.model_url

trainingfolder = os.path.join(os.getenv('HOME'), parent, 'experiments/training')

tarfile = os.path.join(trainingfolder, 'ssd.tar.gz')
os.system('wget {} -O {}'.format(model_url, tarfile))

os.system('tar -xvf {} -C {}'.format(tarfile, trainingfolder))

# os.system('wget https://github.com/rykov8/ssd_keras/archive/master.zip -O {}'.format(modelpath))
# os.system('unzip {} -d {}'.format(modelpath,trainingfolder))
# modelpath = os.path.join(os.getenv('HOME'),'OD/experiments/training','model.zip')
