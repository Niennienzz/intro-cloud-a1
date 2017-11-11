import boto3
import botocore
import datetime
from const.const import Constants
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from models.instance import EC2InstanceModel


class ManagerMetric(Resource):
    """ManagerMetric provides API for manager to get the worker pool metrics.
    """
    @jwt_required()
    def get(self):
        """Get worker pool metrics. (GET)

        Returns:
            (JSON): Worker pool grow/shrink success or fail message.
            (int): HTTP status code.
        """
        # special treat for manager
        if current_identity.id != Constants.MANAGER_DATABASE_ID:
            return {'message': 'you are not manager'}, 403

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
                result = {'instance': item.instance, 'cpu': cpu}
                results.append(result.copy())
        except botocore.exceptions.ClientError as e:
            print(e)
            return [], 500

        return results
