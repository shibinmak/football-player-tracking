"""

** coded by shibinmak on 9/9/18 **
** I pledge to do my best **
** May all beings be Happy,Peaceful,Liberated **

"""
import boto3
import datetime
import time


class AWSSpotInstance:
    @staticmethod
    def request(gpu="p2.xlarge"):
        instance_type = gpu
        print("Starting spot instance of type {}".format(instance_type))
        client = boto3.client('ec2')
        response = client.request_spot_instances(
            DryRun=False,
            SpotPrice='0.30',
            InstanceCount=1,
            Type='one-time',
            LaunchSpecification={
                'ImageId': 'ami-00499ff523cc859e6',
                'KeyName': 'gpu',
                'SecurityGroups': ['all'],
                'InstanceType': instance_type,
                'Placement': {
                    'AvailabilityZone': 'us-west-2a',
                },
                'BlockDeviceMappings': [
                    {
                        'DeviceName': '/dev/sda1',
                        'Ebs': {
                            'SnapshotId': 'snap-007080e536f81dbd0',
                            'VolumeSize': 75,
                            'DeleteOnTermination': True,
                            'VolumeType': 'gp2'
                        },
                    },
                ],
                'EbsOptimized': False,
                'Monitoring': {
                    'Enabled': False
                },
                'SecurityGroupIds': ['']
            })
        print(response)
        print('\n \n')
        time.sleep(10)
        ec2 = boto3.resource('ec2', aws_access_key_id="",
                             aws_secret_access_key="", region_name='')
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print("\nId: {}, type: {}, ip: {}".format(instance.id, instance.instance_type, instance.public_ip_address))
