import boto3
import botocore
import datetime
import threading
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

        average = cpu_sum/len(results)
        print("[Manager Observing - Average CPU Utilization: %s]" % average)
        threading.Timer(5, start_observing, [context]).start()
