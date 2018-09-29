"""

** coded by Shibin Mak on 19/7/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import os
import sys
import time
import boto3
from config import config
from spotinstance import AWSSpotInstance

a = config.aws_acess_key
s = config.aws_secret_key
r = config.aws_region

def zip():
    name = config.parentname
    parent = config.parent
    parent = os.path.dirname(parent)
    zipfile = os.path.join(parent, '{}.zip'.format(name))
    if os.path.isfile(zipfile):
        os.system('sudo rm -r {}'.format(zipfile))

    os.chdir(parent)
    zipcommand = 'zip -r {}.zip {}/'.format(name, name)

    os.system(zipcommand)
    return zipfile


def ip():
    ec2 = boto3.resource('ec2', aws_access_key_id='{}'.format(a),
                         aws_secret_access_key='{}'.format(s), region_name='{}'.format(r))

    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    id = []
    for i in instances:
        id.append(i.id)
    id = id[0]

    instance = ec2.Instance(id=id)
    i = 0
    while True:
        instance = ec2.Instance(id=id)
        status = instance.state['Name']
        time.sleep(1)
        sys.stdout.write(('>' * i) + ("\r [ {} s] ".format(i)))
        sys.stdout.flush()
        i += 1

        if status == 'running':
            break

    ip = instance.public_ip_address
    return ip
zipfile = zip()
aws = AWSSpotInstance()
aws.request()

time.sleep(25)

ip = ip()



aws = 'ssh -i ~/gpu.pem ubuntu@{}'.format(ip)
upload = 'scp -i ~/gpu.pem {} ubuntu@{}:~'.format(zipfile, ip)

os.system(upload)

time.sleep(5)
os.system(aws)
exit(0)
