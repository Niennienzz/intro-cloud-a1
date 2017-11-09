import boto3
import datetime
from botocore.exceptions import ClientError
from const.const import Constants
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity


class ManagerList(Resource):
    """ManagerList provides API for manager to get the worker pool list.
    """

    @jwt_required()
    def get(self):
        # special treat for manager
        if current_identity.id != Constants.MANAGER_ID:
            return {'message': 'you are not manager'}, 403

        # request worker pool status
        results = []
        cw = boto3.client('cloudwatch')
        for key, value in Constants.INSTANCES.items():
            response = cw.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': value
                    },
                ],
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                EndTime=datetime.datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            data_points = response.get('Datapoints', [])
            if len(data_points) == 0:
                status = 'OFF'
                cpu = 0
            else:
                status = 'ON'
                data_point = data_points[len(data_points)-1]
                cpu = data_point.get('Average', '')
            result = {'name': key, 'instance': value, 'status': status, 'cpu': cpu}
            results.append(result.copy())

        return results
