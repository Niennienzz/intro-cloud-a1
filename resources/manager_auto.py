import boto3
import botocore
import datetime
import threading
from botocore.exceptions import ClientError
from const.const import Constants
from models.instance import EC2InstanceModel


def start_observing(context):
    with context:
        # request worker pool status
        results = []
        cw = boto3.client('cloudwatch')
        try:
            for item in EC2InstanceModel.get_all():
                response = cw.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': item.instance,
                        },
                    ],
                    StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
                    EndTime=datetime.datetime.utcnow(),
                    Period=60,
                    Statistics=['Average']
                )
                data_points = response.get('Datapoints', [])
                if len(data_points) == 0:
                    cpu = 0
                else:
                    data_point = data_points[len(data_points)-1]
                    cpu = data_point.get('Average', '')
                results.append(cpu)
        except botocore.exceptions.ClientError as e:
            print(e)
            return [], 500

        cpu_sum = 0
        for cpu in results:
            cpu_sum += cpu

        average = 0
        if len(results) != 0:
            average = cpu_sum/len(results)
            print('[Manager AutoScaling - Average CPU Utilization: %f]' % average)
        else:
            print('[Manager AutoScaling - Average CPU Utilization: 0]')

        if average > 20:
            scale_up(2)
        elif 1 < average < 5:
            scale_down(4)
        else:
            print('[Manager AutoScaling - Balanced]')

        # setup next iteration monitoring
        threading.Timer(5, start_observing, [context]).start()


def scale_up(up_ratio):
    print('[Manager AutoScaling - Scaling Up]')

    ec2_resource = boto3.resource('ec2')
    elb = boto3.client('elb')

    existing = EC2InstanceModel.get_all()
    count = len(existing)
    grow_count = count * up_ratio

    for i in range(count, grow_count):
        try:
            created = ec2_resource.create_instances(
                ImageId=Constants.USER_WORKER_IMAGE_ID,
                InstanceType='t2.small',
                KeyName=Constants.KEY_NAME,
                MaxCount=1,
                MinCount=1,
                Monitoring={
                    'Enabled': True
                },
                SecurityGroups=[
                    Constants.SECURITY_GROUP,
                ],
                DryRun=False,
                InstanceInitiatedShutdownBehavior='terminate',
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'A2-UserWorker-%03d' % (i+1)
                            },
                        ]
                    },
                ]
            )
        except IOError:
            print('[Manager AutoScaling - Scaling Up EC2 %03d Failed]' % (i+1))
            continue

        instance_id = created[0].id

        # add to ELB
        try:
            elb.register_instances_with_load_balancer(
                LoadBalancerName=Constants.ELB_NAME,
                Instances=[
                    {
                        'InstanceId': instance_id
                    },
                ]
            )
        except IOError:
            print('[Manager AutoScaling - Scaling Up ELB %03d Failed]' % (i+1))
            continue

        # add to database
        try:
            item = EC2InstanceModel(instance_id)
            item.save_to_db()
        except IOError:
            print('[Manager AutoScaling - Scaling Up Database %03d Failed]' % (i+1))
            continue

    print('[Manager AutoScaling - Scaling Up Successful]')


def scale_down(down_ratio):
    print('[Manager AutoScaling - Scaling Down]')

    ec2_client = boto3.client('ec2')
    elb = boto3.client('elb')

    existing = EC2InstanceModel.get_all()
    count = len(existing)

    if count == 1:
        print('[Manager AutoScaling - Balanced (Keep One Instance)]')
        return

    for i in range(count):
        if i < count/down_ratio:
            continue

        instance_id = existing[i].instance
        try:
            response = ec2_client.terminate_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print('[Manager AutoScaling - Scaling Down EC2 %03d Failed :%s]' % (count, e))

        # remove from ELB
        try:
            elb.deregister_instances_from_load_balancer(
                LoadBalancerName=Constants.ELB_NAME,
                Instances=[
                    {
                        'InstanceId': instance_id
                    },
                ]
            )
        except IOError:
            print('[Manager AutoScaling - Scaling Down ELB %03d Failed]' % count)

        # remove from database
        try:
            item = EC2InstanceModel.find_by_instance_id(instance_id)
            item.delete_from_db()
        except IOError:
            print('[Manager AutoScaling - Scaling Down Database %03d Failed]' % count)

    print('[Manager AutoScaling - Scaling Down Successful]')
