"""

** coded by shibinmak on 10/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import boto3
import os
import time
import sys
from config import config


def ip():
    print('[INFO] TENSORBOARD http://localhost:8002/')
    a = config.aws_acess_key
    s = config.aws_secret_key
    r = config.aws_region
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


ip = ip()

tb = 'ssh -i ~/gpu.pem -N -f -L 8002:localhost:6006 ubuntu@{}'.format(ip)
# tb = 'ssh -i ~/gpu.pem -L 8002:127.0.0.1:6006 ubuntu@{}'.format(ip)

os.system(tb)

exit(0)
