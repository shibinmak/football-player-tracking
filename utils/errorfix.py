"""

** coded by shibinmak on 9/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
from config import config
parent = config.parentname
print('[INFO] error fixing..')
print("[INFO] replacing 'model_main.py' and 'model_lib.py'")

od = os.path.join(os.getenv('HOME'), 'models/research/object_detection')
mm = os.path.join(od, 'model_main.py')
ml = os.path.join(od, 'model_lib.py')

os.system('rm {}'.format(mm))
os.system('rm {}'.format(ml))

mmnew = os.path.join(os.getenv('HOME'),parent,'utils', 'errorfix', 'model_main.py')
mmcmd = 'cp {} {}'.format(mmnew, od)
mlnew = os.path.join(os.getenv('HOME'),parent,'utils', 'errorfix', 'model_lib.py')
mlcmd = 'cp {} {}'.format(mlnew, od)
os.system(mmcmd)
os.system(mlcmd)

print("[INFO] ERROR FIXED : 'model_main.py' and 'model_lib.py'")
