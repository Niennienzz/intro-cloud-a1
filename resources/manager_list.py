import boto3
import botocore
import datetime
from const.const import Constants
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity


class ManagerList(Resource):
    """ManagerList provides API for manager to get the worker pool statistics.
    """

    @jwt_required()
    def get(self):
        """Get worker pool statistics. (GET)

        Returns:
            (JSON): Worker pool grow/shrink success or fail message.
            (int): HTTP status code.
        """
        # special treat for manager
        if current_identity.id != Constants.MANAGER_ID:
            return {'message': 'you are not manager'}, 403

        # request worker pool status
        results = []
        cw = boto3.client('cloudwatch')
        try:
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
        except botocore.exceptions.ClientError as e:
            print(e)
            return [], 500

        return results
