"""

** coded by shibinmak on 9/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import shutil
import os
import time
import sys
import datetime
from config import config
pf = config.parentfolder
os.system('pip install --user boto3')

time.sleep(5)
import boto3
a = config.aws_acess_key
s = config.aws_secret_key
r = config.aws_region

project = config.PROJECT_NAME
now = datetime.datetime.now().strftime("%b%d%Y%H%M")
parent = config.parent
zname = '{}_MODEL_EXPORTED_{}'.format(project,now)
zsource = os.path.join(parent, 'experiments/exported_model')
archive = os.path.join(parent, '{}.zip'.format(zname))
os.chdir(parent)
print('[INFO] ARCHIVING MODEL FOLDER..')

shutil.make_archive(base_name=zname, format='zip', root_dir=parent, base_dir=zsource)
s3 = boto3.resource('s3',  aws_access_key_id='{}'.format(a),
                         aws_secret_access_key='{}'.format(s), region_name='{}'.format(r))
filename = os.path.basename(archive)
s3.Bucket('makmodels').upload_file(archive, filename)

print('[INFO] SUCESSFULLY UPLOADED TO S3 BUCKET')

time.sleep(15)


def terminate():
    print('[INFO] TERMINATING INSTANCE..')
    ec2 = boto3.resource('ec2', aws_access_key_id=config.aws_acess_key,
                         aws_secret_access_key=config.aws_secret_key, region_name=config.aws_region)

    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    id = []
    for i in instances:
        id.append(i.id)
    id = id[0]

    status = ec2.Instance(id=id).terminate()




terminate()
