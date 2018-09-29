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


def ip():
    print('[INFO] http://localhost:8001/tree/')
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

#aws = 'ssh -i ~/gpu.pem ubuntu@{}'.format(ip)

jp = 'ssh -i ~/gpu.pem -L 8001:localhost:8889 ubuntu@{}'.format(ip)

# os.system(upload)

# time.sleep(5)
# os.system(aws)
os.system(jp)
exit(0)
