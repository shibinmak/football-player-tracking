"""

** coded by shibinmak on 10/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
from config import config
traindir = os.path.join(config.parent,'experiments','training')

tb = 'tensorboard --logdir={} --port 6006'.format(traindir)

os.system(tb)

exit(0)
